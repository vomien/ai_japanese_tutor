from app.models.user_profile import UserProfile

class UserProfileService:

    @staticmethod
    def get_profile(
        db,
        user_id
    ):
        return (
            db.query(UserProfile)
            .filter(
                UserProfile.user_id == user_id
            ).first()
        )