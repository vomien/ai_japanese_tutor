from app.models.message import Message

class ChatHistoryService:

    @staticmethod
    def save_message(
        db,
        conversation_id,
        role,
        content
    ):

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def get_messages(
        db,
        conversation_id
    ):

        messages = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.id)
            .all()
        )

        return messages