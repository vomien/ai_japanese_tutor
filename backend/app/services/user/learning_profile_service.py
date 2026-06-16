from app.models.learning_profile import(
    LearningProfile
)

class LearningProfileService:

    @staticmethod
    def get_profile(
        db,
        user_id
    ):
        return(
            db.query(LearningProfile)
            .filter(
                LearningProfile.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def update_weakness(
        db,
        user_id,
        weakness
    ):
        profile = (
            db.query(LearningProfile)
            .filter(
                LearningProfile.user_id == user_id
            ).first()
        )

        if not profile:
            return
        
        if weakness not in profile.weaknesses:
            profile.weaknesses += f", {weakness}"
        
        db.commit()