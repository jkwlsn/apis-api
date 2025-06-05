DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS apiaries CASCADE;
DROP TABLE IF EXISTS hives CASCADE;
DROP TABLE IF EXISTS colonies CASCADE;
DROP TYPE IF EXISTS queen_colour CASCADE;
DROP TABLE IF EXISTS queens CASCADE;
DROP TABLE IF EXISTS inspections CASCADE;
DROP TABLE IF EXISTS observations CASCADE;
DROP TABLE IF EXISTS actions CASCADE;

-- User table
CREATE TABLE IF NOT EXISTS users (
    user_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL
);

-- User sessions table
CREATE TABLE IF NOT EXISTS sessions (
    session_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_start timestamptz NOT NULL,
    user_id int NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
);

-- Apiaries table
CREATE TABLE IF NOT EXISTS apiaries (
    apiary_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    location text NOT NULL,
    user_id integer NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
);

-- Hives table
CREATE TABLE IF NOT EXISTS hives (
    hive_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    apiary_id integer NOT NULL REFERENCES apiaries(apiary_id) ON DELETE CASCADE
);

-- Colonies table
CREATE TABLE IF NOT EXISTS colonies (
    colony_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hive_id integer NOT NULL REFERENCES hives(hive_id) ON DELETE CASCADE
);

-- Queen colour enum
CREATE TYPE queen_colour AS ENUM (
    'White',
    'Yellow',
    'Red',
    'Green',
    'Blue',
    'Unmarked'
);

-- Queens table
CREATE TABLE IF NOT EXISTS queens (
    queen_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    colour queen_colour NOT NULL,
    clipped boolean NOT NULL,
    colony_id integer NOT NULL REFERENCES colonies(colony_id) ON DELETE CASCADE
);

-- Inspections table
CREATE TABLE IF NOT EXISTS inspections (
    inspection_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    inspection_timestamp timestamptz NOT NULL,
    colony_id integer NOT NULL REFERENCES colonies(colony_id) ON DELETE CASCADE
);

-- Observations table
CREATE TABLE IF NOT EXISTS observations (
    observation_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    queenright boolean NOT NULL,
    queen_cells integer NOT NULL,
    bias boolean NOT NULL,
    brood_frames integer NOT NULL,
    store_frames integer NOT NULL,
    chalk_brood boolean NOT NULL,
    foul_brood boolean NOT NULL,
    varroa_count integer NOT NULL,
    temper integer NOT NULL,
    notes text,
    inspection_id integer NOT NULL REFERENCES inspections(
        inspection_id
    ) ON DELETE CASCADE
);

-- Actions table
CREATE TABLE IF NOT EXISTS actions (
    action_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    notes text,
    inspection_id integer NOT NULL REFERENCES inspections(
        inspection_id
    ) ON DELETE CASCADE
);
