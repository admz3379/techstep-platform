from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from ..db.database import Base


class PodcastStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class EpisodeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    ARCHIVED = "archived"


class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String, nullable=True)
    cover_image_url = Column(String, nullable=True)
    host_name = Column(String, nullable=False)
    host_bio = Column(Text, nullable=True)
    host_avatar_url = Column(String, nullable=True)
    category = Column(String, nullable=False)
    language = Column(String, default="en", nullable=False)
    status = Column(SQLEnum(PodcastStatus), default=PodcastStatus.DRAFT, nullable=False)
    is_featured = Column(Boolean, default=False)
    subscriber_count = Column(Integer, default=0)
    total_plays = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    rss_feed_url = Column(String, nullable=True)
    apple_podcasts_url = Column(String, nullable=True)
    spotify_url = Column(String, nullable=True)
    google_podcasts_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    episodes = relationship("PodcastEpisode", back_populates="podcast")


class PodcastEpisode(Base):
    __tablename__ = "podcast_episodes"

    id = Column(Integer, primary_key=True, index=True)
    podcast_id = Column(Integer, ForeignKey("podcasts.id"), nullable=False)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String, nullable=True)
    audio_url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    duration_seconds = Column(Integer, nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    episode_number = Column(Integer, nullable=True)
    season_number = Column(Integer, nullable=True)
    status = Column(SQLEnum(EpisodeStatus), default=EpisodeStatus.DRAFT, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    play_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    transcript = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)  # JSON string
    guest_name = Column(String, nullable=True)
    guest_bio = Column(Text, nullable=True)
    guest_avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    podcast = relationship("Podcast", back_populates="episodes")