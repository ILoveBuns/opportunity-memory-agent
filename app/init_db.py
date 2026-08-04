from .repository import Repository


SCHEMA = """
CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY,
    name STRING NOT NULL,
    reward_usd INT8 NOT NULL CHECK (reward_usd >= 0),
    deadline TIMESTAMPTZ NULL,
    confidence FLOAT8 NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    status STRING NOT NULL CHECK (status IN ('candidate','active','blocked','submitted','closed')),
    next_action STRING NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memory_events (
    id UUID PRIMARY KEY,
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    kind STRING NOT NULL CHECK (kind IN ('created','review','progress','blocker','submission')),
    detail STRING NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    INDEX (opportunity_id, created_at)
);

CREATE TABLE IF NOT EXISTS executions (
    id UUID PRIMARY KEY,
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    action_kind STRING NOT NULL CHECK (action_kind IN ('verify_evidence_sha256')),
    state STRING NOT NULL CHECK (state IN ('planned','approved','succeeded','failed')),
    input JSONB NOT NULL,
    result JSONB NULL,
    approval_note STRING NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    INDEX (opportunity_id, created_at)
);
"""


def main():
    repository = Repository()
    with repository.connection() as connection:
        connection.execute(SCHEMA)
        connection.commit()


if __name__ == "__main__":
    main()
