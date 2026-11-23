"""Mini-games that earn coins. No betting."""
import random

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import check_cooldown, fmt


class TriviaButton(discord.ui.Button):
    def __init__(self, answer: str, is_correct: bool):
        # Discord enforces a strict 80-character max on button labels
        display_label = answer if len(answer) <= 80 else f"{answer[:77]}..."
        super().__init__(
            label=display_label,
            style=discord.ButtonStyle.secondary,
        )
        self.answer = answer
        self.is_correct = is_correct

    async def callback(self, interaction: discord.Interaction):
        view: TriviaView = self.view
        await view.handle_answer(interaction, self)


class TriviaView(discord.ui.View):
    def __init__(
        self,
        author_id: int,
        question: str,
        correct: str,
        options: list[str],
        db,
        reward: int,
        timeout: float,
    ):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.question = question
        self.correct = correct
        self.db = db
        self.reward = reward
        self.answered = False
        self.message: discord.Message | None = None

        for option in options:
            self.add_item(TriviaButton(answer=option, is_correct=(option == correct)))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This isn't your trivia question! Run `/trivia` to start your own.",
                ephemeral=True,
            )
            return False
        return True

    def _reveal(self, chosen_button: TriviaButton | None = None):
        for child in self.children:
            if isinstance(child, TriviaButton):
                child.disabled = True
                if child.is_correct:
                    child.style = discord.ButtonStyle.success
                elif chosen_button is not None and child is chosen_button:
                    child.style = discord.ButtonStyle.danger

    async def handle_answer(
        self, interaction: discord.Interaction, chosen_button: TriviaButton
    ):
        if self.answered:
            return
        self.answered = True
        self.stop()
        self._reveal(chosen_button)

        if chosen_button.is_correct:
            self.db.add_wallet(self.author_id, self.reward)
            result_text = (
                f"**{self.question}**\n\n"
                f"✅ Correct! You earned {fmt(self.reward)}."
            )
        else:
            result_text = (
                f"**{self.question}**\n\n"
                f"❌ Wrong! You picked **{chosen_button.answer}**, "
                f"but the correct answer was **{self.correct}**."
            )

        await interaction.response.edit_message(content=result_text, view=self)

    async def on_timeout(self):
        if self.answered:
            return
        self.answered = True
        self._reveal(chosen_button=None)
        if self.message:
            try:
                await self.message.edit(
                    content=f"**{self.question}**\n\n⏰ Time's up! The correct answer was **{self.correct}**.",
                    view=self,
                )
            except discord.HTTPException:
                pass


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db
        self._user_pools: dict[int, list[tuple[str, str, list[str]]]] = {}

    def _next_question(self, user_id: int) -> tuple[str, str, list[str]]:
        pool = self._user_pools.get(user_id)
        if not pool:
            pool = list(config.TRIVIA_QUESTIONS)
            random.shuffle(pool)
            self._user_pools[user_id] = pool
        return pool.pop()

    @app_commands.command(description="Answer a multiple-choice question to win coins.")
    async def trivia(self, interaction: discord.Interaction):
        if await check_cooldown(self.db, interaction, "trivia", config.TRIVIA_COOLDOWN):
            return

        question, correct, wrongs = self._next_question(interaction.user.id)
        options = [correct, *wrongs]
        random.shuffle(options)

        view = TriviaView(
            author_id=interaction.user.id,
            question=question,
            correct=correct,
            options=options,
            db=self.db,
            reward=config.TRIVIA_REWARD,
            timeout=config.TRIVIA_TIMEOUT,
        )
        await interaction.response.send_message(
            f"🧠 **Trivia:** {question}\n"
            f"You have {config.TRIVIA_TIMEOUT}s to answer for {fmt(config.TRIVIA_REWARD)}!",
            view=view,
        )
        # Only start the cooldown once the question was actually delivered
        self.db.set_cooldown(interaction.user.id, "trivia")
        view.message = await interaction.original_response()

    # TODO: /rps <rock|paper|scissors>     - beat the bot for RPS_REWARD


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))