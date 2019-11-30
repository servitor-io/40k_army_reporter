"""initial revision

Revision ID: 445de4e3108d
Revises: 
Create Date: 2019-11-30 14:54:13.498217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '445de4e3108d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('figure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('figure_type', sa.Text(), nullable=True),
    sa.Column('figure_name', sa.Text(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('move', sa.Text(), nullable=True),
    sa.Column('weapon_skill', sa.Integer(), nullable=True),
    sa.Column('ballistic_skill', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Text(), nullable=True),
    sa.Column('toughness', sa.Text(), nullable=True),
    sa.Column('wounds', sa.Text(), nullable=True),
    sa.Column('attacks', sa.Text(), nullable=True),
    sa.Column('leadership', sa.Text(), nullable=True),
    sa.Column('save', sa.Text(), nullable=True),
    sa.Column('max_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.Text(), nullable=True),
    sa.Column('names', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('player_name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('wargear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('profile', sa.Text(), nullable=True),
    sa.Column('wargear_range', sa.Text(), nullable=True),
    sa.Column('wargear_type', sa.Text(), nullable=True),
    sa.Column('strength', sa.Text(), nullable=True),
    sa.Column('ap', sa.Text(), nullable=True),
    sa.Column('damage', sa.Text(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('keyword_id', sa.Integer(), nullable=True),
    sa.Column('is_subfaction', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('figure_ability_secondary',
    sa.Column('figure_id', sa.Integer(), nullable=True),
    sa.Column('ability_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ability_id'], ['ability.id'], ),
    sa.ForeignKeyConstraint(['figure_id'], ['figure.id'], )
    )
    op.create_table('figure_keyword_secondary',
    sa.Column('figure_id', sa.Integer(), nullable=True),
    sa.Column('keyword_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['figure_id'], ['figure.id'], ),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], )
    )
    op.create_table('tactic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('keyword_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role_secondary',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_roster_secondary',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('roster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roster_id'], ['roster.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('wargear_ability_secondary',
    sa.Column('wargear_id', sa.Integer(), nullable=True),
    sa.Column('ability_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ability_id'], ['ability.id'], ),
    sa.ForeignKeyConstraint(['wargear_id'], ['wargear.id'], )
    )
    op.create_table('faction_ability_secondary',
    sa.Column('faction_id', sa.Integer(), nullable=True),
    sa.Column('ability_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ability_id'], ['ability.id'], ),
    sa.ForeignKeyConstraint(['faction_id'], ['faction.id'], )
    )
    op.create_table('figure_faction_secondary',
    sa.Column('figure_id', sa.Integer(), nullable=True),
    sa.Column('faction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faction_id'], ['faction.id'], ),
    sa.ForeignKeyConstraint(['figure_id'], ['figure.id'], )
    )
    op.create_table('roster_faction_secondary',
    sa.Column('roster_id', sa.Integer(), nullable=True),
    sa.Column('faction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faction_id'], ['faction.id'], ),
    sa.ForeignKeyConstraint(['roster_id'], ['roster.id'], )
    )
    op.create_table('specialization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('tactic_id', sa.Integer(), nullable=True),
    sa.Column('passive', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['tactic_id'], ['tactic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tactic_faction_secondary',
    sa.Column('tactic_id', sa.Integer(), nullable=True),
    sa.Column('faction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faction_id'], ['faction.id'], ),
    sa.ForeignKeyConstraint(['tactic_id'], ['tactic.id'], )
    )
    op.create_table('rosterentry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('figure_id', sa.Integer(), nullable=True),
    sa.Column('specialization_id', sa.Integer(), nullable=True),
    sa.Column('roster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['figure_id'], ['figure.id'], ),
    sa.ForeignKeyConstraint(['roster_id'], ['roster.id'], ),
    sa.ForeignKeyConstraint(['specialization_id'], ['specialization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rosterentry_wargear_secondary',
    sa.Column('rosterentry_id', sa.Integer(), nullable=True),
    sa.Column('wargear_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rosterentry_id'], ['rosterentry.id'], ),
    sa.ForeignKeyConstraint(['wargear_id'], ['wargear.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rosterentry_wargear_secondary')
    op.drop_table('rosterentry')
    op.drop_table('tactic_faction_secondary')
    op.drop_table('specialization')
    op.drop_table('roster_faction_secondary')
    op.drop_table('figure_faction_secondary')
    op.drop_table('faction_ability_secondary')
    op.drop_table('wargear_ability_secondary')
    op.drop_table('user_roster_secondary')
    op.drop_table('user_role_secondary')
    op.drop_table('tactic')
    op.drop_table('figure_keyword_secondary')
    op.drop_table('figure_ability_secondary')
    op.drop_table('faction')
    op.drop_table('wargear')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('roster')
    op.drop_table('role')
    op.drop_table('keyword')
    op.drop_table('figure')
    op.drop_table('ability')
    # ### end Alembic commands ###