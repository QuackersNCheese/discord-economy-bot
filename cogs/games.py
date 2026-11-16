"""Mini-games that earn coins. No betting."""

import random

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import check_cooldown, fmt


class TriviaButton(discord.ui.Button["TriviaView"]):
    def __init__(self, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.answer = label

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        await self.view.handle_answer(interaction, self.answer)


class TriviaView(discord.ui.View):
    def __init__(self, asker: discord.abc.User, correct: str, db, base_content: str):
        super().__init__(timeout=config.TRIVIA_TIMEOUT)
        self.asker_id = asker.id
        self.correct = correct
        self.db = db
        self.base_content = base_content
        self.answered = False
        self.message: discord.Message | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.asker_id:
            await interaction.response.send_message(
                "This trivia question isn't for you.", ephemeral=True
            )
            return False
        return True

    def _reveal(self, chosen: str | None = None):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
                if child.label == self.correct:
                    child.style = discord.ButtonStyle.success
                elif chosen is not None and child.label == chosen:
                    child.style = discord.ButtonStyle.danger

    async def handle_answer(self, interaction: discord.Interaction, answer: str):
        if self.answered:
            return
        self.answered = True
        self.stop()
        self._reveal(answer)
        if answer == self.correct:
            self.db.add_wallet(self.asker_id, config.TRIVIA_REWARD)
            result = f"✅ Correct! You earned {fmt(config.TRIVIA_REWARD)}."
        else:
            result = f"❌ Wrong! The correct answer was **{self.correct}**."
        await interaction.response.edit_message(
            content=f"{self.base_content}\n\n{result}", view=self
        )

    async def on_timeout(self):
        if self.answered:
            return
        self.answered = True
        self._reveal()
        if self.message:
            try:
                await self.message.edit(
                    content=(
                        f"{self.base_content}\n\n"
                        f"⏰ Time's up! The correct answer was **{self.correct}**."
                    ),
                    view=self,
                )
            except discord.HTTPException:
                pass


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(description="Answer a multiple-choice question to win coins.")
    async def trivia(self, interaction: discord.Interaction):
        if await check_cooldown(self.db, interaction, "trivia", config.TRIVIA_COOLDOWN):
            return

        question, correct, wrongs = random.choice(config.TRIVIA_QUESTIONS)
        answers = [correct, *wrongs]
        random.shuffle(answers)

        content = (
            f"🧠 **Trivia:** {question}\n"
            f"You have {config.TRIVIA_TIMEOUT}s to answer for {fmt(config.TRIVIA_REWARD)}!"
        )
        view = TriviaView(interaction.user, correct, self.db, content)
        for answer in answers:
            view.add_item(TriviaButton(answer))

        self.db.set_cooldown(interaction.user.id, "trivia")
        await interaction.response.send_message(content, view=view)
        view.message = await interaction.original_response()


# TODO: /rps <rock|paper|scissors>     - beat the bot for RPS_REWARD


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
