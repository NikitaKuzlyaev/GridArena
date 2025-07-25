# import datetime
#
# from sqlalchemy import String, DateTime, Integer, UniqueConstraint
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.sql import functions as sqlalchemy_functions
#
# from core.database.connection import Base
#
#
# class UserAuth(Base):
#     __tablename__ = "user_auth"
#
#     id: Mapped[int] = mapped_column(
#         primary_key=True
#     )
#
#     user_id
#
#     refresh_token
#
#     banned_access_token
#
#     created_at: Mapped[datetime.datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=sqlalchemy_functions.now()
#     )
