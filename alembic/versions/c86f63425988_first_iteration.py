from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c86f63425988'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Создаем тип ENUM только если он еще не существует
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN
            CREATE TYPE role AS ENUM('admin', 'user');
        END IF;
    END
    $$;
    """)
    # Добавьте другие операции миграции здесь

def downgrade():
    op.execute("DROP TYPE role")
    # Добавьте операции отката миграции здесь
