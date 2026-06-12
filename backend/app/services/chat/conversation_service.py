from app.models.conversation import Conversation


class ConversationService:

    @staticmethod
    def create_conversation(
        db,
        user_id,
        title
    ):

        conversation = Conversation(
            user_id=user_id,
            title=title
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation