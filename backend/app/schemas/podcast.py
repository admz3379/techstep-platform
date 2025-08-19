from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.podcast import PodcastStatus, EpisodeStatus


class PodcastBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    short_description: Optional[str] = None
    host_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=100)
    language: str = "en"


class PodcastCreate(PodcastBase):
    slug: str = Field(..., min_length=1, max_length=200)
    cover_image_url: Optional[str] = None
    host_bio: Optional[str] = None
    host_avatar_url: Optional[str] = None
    apple_podcasts_url: Optional[str] = None
    spotify_url: Optional[str] = None
    google_podcasts_url: Optional[str] = None


class PodcastUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    short_description: Optional[str] = None
    host_name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    language: Optional[str] = None
    cover_image_url: Optional[str] = None
    host_bio: Optional[str] = None
    host_avatar_url: Optional[str] = None
    status: Optional[PodcastStatus] = None
    is_featured: Optional[bool] = None
    apple_podcasts_url: Optional[str] = None
    spotify_url: Optional[str] = None
    google_podcasts_url: Optional[str] = None


class PodcastResponse(PodcastBase):
    id: int
    slug: str
    cover_image_url: Optional[str] = None
    host_bio: Optional[str] = None
    host_avatar_url: Optional[str] = None
    status: PodcastStatus
    is_featured: bool
    subscriber_count: int
    total_plays: int
    rating: float
    rating_count: int
    rss_feed_url: Optional[str] = None
    apple_podcasts_url: Optional[str] = None
    spotify_url: Optional[str] = None
    google_podcasts_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PodcastEpisodeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    short_description: Optional[str] = None
    duration_seconds: int = Field(..., gt=0)


class PodcastEpisodeCreate(PodcastEpisodeBase):
    podcast_id: int
    slug: str = Field(..., min_length=1, max_length=200)
    audio_url: str = Field(..., min_length=1)
    thumbnail_url: Optional[str] = None
    episode_number: Optional[int] = Field(None, gt=0)
    season_number: Optional[int] = Field(None, gt=0)
    file_size_bytes: Optional[int] = Field(None, gt=0)
    transcript: Optional[str] = None
    keywords: Optional[List[str]] = None
    guest_name: Optional[str] = None
    guest_bio: Optional[str] = None
    guest_avatar_url: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class PodcastEpisodeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    short_description: Optional[str] = None
    audio_url: Optional[str] = Field(None, min_length=1)
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = Field(None, gt=0)
    episode_number: Optional[int] = Field(None, gt=0)
    season_number: Optional[int] = Field(None, gt=0)
    file_size_bytes: Optional[int] = Field(None, gt=0)
    status: Optional[EpisodeStatus] = None
    published_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    transcript: Optional[str] = None
    keywords: Optional[List[str]] = None
    guest_name: Optional[str] = None
    guest_bio: Optional[str] = None
    guest_avatar_url: Optional[str] = None


class PodcastEpisodeResponse(PodcastEpisodeBase):
    id: int
    podcast_id: int
    slug: str
    audio_url: str
    thumbnail_url: Optional[str] = None
    episode_number: Optional[int] = None
    season_number: Optional[int] = None
    file_size_bytes: Optional[int] = None
    status: EpisodeStatus
    published_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    play_count: int
    download_count: int
    likes_count: int
    transcript: Optional[str] = None
    keywords: Optional[List[str]] = None
    guest_name: Optional[str] = None
    guest_bio: Optional[str] = None
    guest_avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Podcast info
    podcast_title: Optional[str] = None

    class Config:
        from_attributes = True