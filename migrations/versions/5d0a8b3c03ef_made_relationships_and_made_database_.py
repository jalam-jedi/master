from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '5d0a8b3c03ef'
down_revision = '00cd5f454ae3'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # Check if the new tables already exist
    existing_tables = connection.execute(text(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )).fetchall()
    existing_table_names = {table[0] for table in existing_tables}

    # Step 1: Create new tables with the updated structure if they do not exist
    if 'gis_model_new' not in existing_table_names:
        op.create_table(
            'gis_model_new',
            sa.Column('ID', sa.Integer(), nullable=False),
            sa.Column('ImagePath', sa.String(length=2000), nullable=False),
            sa.Column('Name', sa.String(length=100), nullable=False),
            sa.Column('Latitude', sa.Float(precision=20), nullable=False),
            sa.Column('Longitude', sa.Float(), nullable=False),
            sa.Column('Comments', sa.String(length=1000), nullable=True),
            sa.Column('Source', sa.String(length=50), nullable=True),
            sa.Column('Date', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.PrimaryKeyConstraint('ID')
        )

    if 'analysis_model_new' not in existing_table_names:
        op.create_table(
            'analysis_model_new',
            sa.Column('ImageID', sa.Integer(), nullable=False),
            sa.Column('Location_Type', sa.String(length=500), nullable=False),
            sa.Column('Unique_Feature', sa.String(length=500), nullable=False),
            sa.Column('Geographical_Feature', sa.String(length=500), nullable=False),
            sa.Column('Climate', sa.String(length=500), nullable=False),
            sa.ForeignKeyConstraint(['ImageID'], ['gis_model_new.ID'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('ImageID')
        )

    if 'comp_model_new' not in existing_table_names:
        op.create_table(
            'comp_model_new',
            sa.Column('ImageID', sa.Integer(), nullable=False),
            sa.Column('Hist_Relevance', sa.String(length=500), nullable=False),
            sa.Column('Mod_Imp', sa.String(length=500), nullable=False),
            sa.Column('Comp_Analysis', sa.String(length=500), nullable=False),
            sa.Column('Insight', sa.String(length=500), nullable=False),
            sa.ForeignKeyConstraint(['ImageID'], ['gis_model_new.ID'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('ImageID')
        )

    # Step 2: Migrate data from old tables to new tables
    existing_table_names = {table[0] for table in existing_tables}

    if 'gis__model' in existing_table_names:
        connection.execute(text("""
            INSERT INTO gis_model_new (ID, ImagePath, Name, Latitude, Longitude, Comments, Source, Date)
            SELECT ID, ImagePath, Name, Latitude, Longitude, Comments, Source, Date FROM gis__model
        """))

    if 'analysis__model' in existing_table_names:
        connection.execute(text("""
            INSERT INTO analysis_model_new (ImageID, Location_Type, Unique_Feature, Geographical_Feature, Climate)
            SELECT ImageID, Location_Type, Unique_Feature, Geographical_Feature, Climate FROM analysis__model
        """))

    if 'comp__model' in existing_table_names:
        connection.execute(text("""
            INSERT INTO comp_model_new (ImageID, Hist_Relevance, Mod_Imp, Comp_Analysis, Insight)
            SELECT ImageID, Hist_Relevance, Mod_Imp, Comp_Analysis, Insight FROM comp__model
        """))

    # Step 3: Drop old tables if they exist
    if 'gis__model' in existing_table_names:
        op.drop_table('gis__model')
    if 'analysis__model' in existing_table_names:
        op.drop_table('analysis__model')
    if 'comp__model' in existing_table_names:
        op.drop_table('comp__model')

    # Step 4: Rename new tables to original names
    op.rename_table('gis_model_new', 'gis_model')
    op.rename_table('analysis_model_new', 'analysis_model')
    op.rename_table('comp_model_new', 'comp_model')


def downgrade():
    connection = op.get_bind()

    # Check if the new tables exist before trying to downgrade
    existing_tables = connection.execute(text(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )).fetchall()
    existing_table_names = {table[0] for table in existing_tables}

    # Step 1: Recreate old tables if they do not exist
    if 'gis__model' not in existing_table_names:
        op.create_table(
            'gis__model',
            sa.Column('ID', sa.Integer(), nullable=False),
            sa.Column('ImagePath', sa.String(length=2000), nullable=False),
            sa.Column('Name', sa.String(length=100), nullable=False),
            sa.Column('Latitude', sa.Float(precision=20), nullable=False),
            sa.Column('Longitude', sa.Float(), nullable=False),
            sa.Column('Comments', sa.String(length=1000), nullable=True),
            sa.Column('Source', sa.String(length=50), nullable=True),
            sa.Column('Date', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('ID')
        )

    if 'analysis__model' not in existing_table_names:
        op.create_table(
            'analysis__model',
            sa.Column('ImageID', sa.Integer(), nullable=False),
            sa.Column('ImagePath', sa.String(length=2000), nullable=False),
            sa.Column('Name', sa.String(length=100), nullable=False),
            sa.Column('Location_Type', sa.String(length=500), nullable=False),
            sa.Column('Unique_Feature', sa.String(length=500), nullable=False),
            sa.Column('Geographical_Feature', sa.String(length=500), nullable=False),
            sa.Column('Climate', sa.String(length=500), nullable=False),
            sa.PrimaryKeyConstraint('ImageID')
        )

    if 'comp__model' not in existing_table_names:
        op.create_table(
            'comp__model',
            sa.Column('ImageID', sa.Integer(), nullable=False),
            sa.Column('ImagePath', sa.String(length=2000), nullable=False),
            sa.Column('Name', sa.String(length=100), nullable=False),
            sa.Column('Hist_Relevance', sa.String(length=500), nullable=False),
            sa.Column('Mod_Imp', sa.String(length=500), nullable=False),
            sa.Column('Comp_Analysis', sa.String(length=500), nullable=False),
            sa.Column('Insight', sa.String(length=500), nullable=False),
            sa.PrimaryKeyConstraint('ImageID')
        )

    # Step 2: Migrate data back from new tables to old tables
    if 'gis_model' in existing_table_names:
        connection.execute("""
            INSERT INTO gis__model (ID, ImagePath, Name, Latitude, Longitude, Comments, Source, Date)
            SELECT ID, ImagePath, Name, Latitude, Longitude, Comments, Source, Date FROM gis_model
        """)

    if 'analysis_model' in existing_table_names:
        connection.execute("""
            INSERT INTO analysis__model (ImageID, ImagePath, Name, Location_Type, Unique_Feature, Geographical_Feature, Climate)
            SELECT ImageID, NULL, NULL, Location_Type, Unique_Feature, Geographical_Feature, Climate FROM analysis_model
        """)

    if 'comp_model' in existing_table_names:
        connection.execute("""
            INSERT INTO comp__model (ImageID, ImagePath, Name, Hist_Relevance, Mod_Imp, Comp_Analysis, Insight)
            SELECT ImageID, NULL, NULL, Hist_Relevance, Mod_Imp, Comp_Analysis, Insight FROM comp_model
        """)

    # Step 3: Drop new tables if they exist
    if 'gis_model' in existing_table_names:
        op.drop_table('gis_model')
    if 'analysis_model' in existing_table_names:
        op.drop_table('analysis_model')
    if 'comp_model' in existing_table_names:
        op.drop_table('comp_model')
