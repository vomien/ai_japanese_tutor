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

    @staticmethod
    def get_conversation(
        db,
        user_id
    ):
        return(
            db.query(Conversation). filter(Conversation.user_id == user_id).all()
        )
    
    @staticmethod
    def get_by_id(
        db,
        conversation_id
    ):
        return(
            db.query(Conversation).filter(Conversation.id == conversation_id).first()
        )

    @staticmethod
    def update_title(
        db,
        conversation_id,
        title
    ):
        conversation = (
            db.query(Conversation).filter(Conversation.id == conversation_id).first()
        )
        
        if conversation:
        
            conversation.title = title
        
            db.commit()
        
            db.refresh(conversation)
        
        return conversation
