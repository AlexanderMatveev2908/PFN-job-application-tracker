CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);

INSERT INTO alembic_version (version_num)
VALUES (<curr_head_id>);
