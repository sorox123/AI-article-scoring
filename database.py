"""
Database models and connection management for the article scoring app.
Uses SQLAlchemy ORM with PostgreSQL backend for persistent, multi-user storage.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.pool import QueuePool
from datetime import datetime
import os
import json

Base = declarative_base()


class Article(Base):
    """Article model - stores URLs and titles"""
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(2048), unique=True, nullable=False, index=True)
    title = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to scores
    scores = relationship('Score', back_populates='article', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'URL': self.url,
            'Title': self.title
        }


class Score(Base):
    """Score model - stores individual peer scores for articles"""
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False, index=True)
    
    # Scoring categories
    accuracy = Column(Integer, nullable=False)
    credibility = Column(Integer, nullable=False)
    citation = Column(Integer, nullable=False)
    reasoning = Column(Integer, nullable=False)
    confidence = Column(Integer, nullable=False)
    
    notes = Column(Text, default='')
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to article
    article = relationship('Article', back_populates='scores')
    
    def to_dict(self):
        return {
            'accuracy': self.accuracy,
            'credibility': self.credibility,
            'citation': self.citation,
            'reasoning': self.reasoning,
            'confidence': self.confidence,
            'notes': self.notes,
            'timestamp': self.timestamp.isoformat()
        }


class DatabaseManager:
    """Manages database connections and provides data access methods"""
    
    def __init__(self, database_url=None):
        """
        Initialize database connection
        
        Args:
            database_url: PostgreSQL connection string. If None, uses DATABASE_URL env var
                         or falls back to SQLite for local development
        """
        if database_url is None:
            database_url = os.environ.get('DATABASE_URL')
            
            # Fix for Render's postgres:// vs postgresql:// issue
            if database_url and database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            # Fallback to SQLite for local development
            if not database_url:
                database_url = 'sqlite:///article_scores.db'
        
        # Create engine with connection pooling
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True  # Verify connections before using
        )
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
    
    def get_session(self):
        """Get a database session"""
        return self.Session()
    
    def close_session(self):
        """Close the current session"""
        self.Session.remove()
    
    # Article operations
    
    def get_all_articles(self):
        """Get all articles as list of dicts"""
        session = self.get_session()
        try:
            articles = session.query(Article).order_by(Article.created_at.desc()).all()
            return [article.to_dict() for article in articles]
        finally:
            session.close()
    
    def add_articles(self, articles_data):
        """
        Add multiple articles, skipping duplicates
        
        Args:
            articles_data: List of dicts with 'URL' and 'Title' keys
            
        Returns:
            Tuple of (merged_articles, new_count, duplicates)
        """
        session = self.get_session()
        try:
            new_count = 0
            duplicates = []
            
            for article_data in articles_data:
                url = article_data['URL']
                title = article_data['Title']
                
                # Check if article already exists
                existing = session.query(Article).filter_by(url=url).first()
                
                if existing:
                    # Duplicate found - check by title as well for reporting
                    if existing.title.lower() == title.lower():
                        duplicates.append(title)
                else:
                    # New article
                    article = Article(url=url, title=title)
                    session.add(article)
                    new_count += 1
            
            session.commit()
            
            # Get all articles to return
            all_articles = self.get_all_articles()
            
            return all_articles, new_count, duplicates
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_article_by_url(self, url):
        """Get article by URL"""
        session = self.get_session()
        try:
            return session.query(Article).filter_by(url=url).first()
        finally:
            session.close()
    
    # Score operations
    
    def get_all_scores(self):
        """
        Get all scores in the format expected by the app
        
        Returns:
            Dict mapping URLs to lists of score dicts
        """
        session = self.get_session()
        try:
            articles = session.query(Article).all()
            scores_data = {}
            
            for article in articles:
                if article.scores:
                    scores_data[article.url] = [score.to_dict() for score in article.scores]
            
            return scores_data
        finally:
            session.close()
    
    def get_scores_for_article(self, url):
        """Get all scores for a specific article URL"""
        session = self.get_session()
        try:
            article = session.query(Article).filter_by(url=url).first()
            if article:
                return [score.to_dict() for score in article.scores]
            return []
        finally:
            session.close()
    
    def add_score(self, url, score_data):
        """
        Add a score for an article
        
        Args:
            url: Article URL
            score_data: Dict with scoring category values
        """
        session = self.get_session()
        try:
            # Get or create article
            article = session.query(Article).filter_by(url=url).first()
            if not article:
                # Article doesn't exist - create it with URL as title
                article = Article(url=url, title=url[:100])
                session.add(article)
                session.flush()  # Get the ID
            
            # Create score
            score = Score(
                article_id=article.id,
                accuracy=score_data['accuracy'],
                credibility=score_data['credibility'],
                citation=score_data['citation'],
                reasoning=score_data['reasoning'],
                confidence=score_data['confidence'],
                notes=score_data.get('notes', '')
            )
            
            session.add(score)
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_statistics(self):
        """Get database statistics"""
        session = self.get_session()
        try:
            total_articles = session.query(Article).count()
            total_scores = session.query(Score).count()
            
            # Articles with at least one score
            articles_with_scores = session.query(Article).filter(
                Article.scores.any()
            ).count()
            
            articles_without_scores = total_articles - articles_with_scores
            
            return {
                'total_articles': total_articles,
                'total_scores': total_scores,
                'articles_with_scores': articles_with_scores,
                'articles_without_scores': articles_without_scores
            }
        finally:
            session.close()


# Global database manager instance
db_manager = None


def init_db(database_url=None):
    """Initialize the global database manager"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    return db_manager


def get_db():
    """Get the global database manager instance"""
    global db_manager
    if db_manager is None:
        db_manager = init_db()
    return db_manager
