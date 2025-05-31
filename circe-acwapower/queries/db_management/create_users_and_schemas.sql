--SQL Script to create the users and schemas for the project

-- NOTE: Passwords are not provided here. Fill them before running the query,
-- but don't commit any file with a password

-- Create USERS
-- 1. User dev. For development. Needs to write and read from every schema. In 
--    the future we could deny access to raw input, once acwa takes care of it
-- 2. User powerbi. For visualization. Only needs to have read access to output
--    tables
-- 3. User acwa. For input. Only needs to write at the input schema.

CREATE USER dev WITH PASSWORD = '';
CREATE USER powerbi WITH PASSWORD = '';
CREATE USER acwa WITH PASSWORD = '';

-- Create SCHEMAS
-- 1. raw: For raw input data
-- 2. intermediate: Intermediate tables that are only meant to be accessed by 
--     dev as a checkpoint of a longer process
-- 3. vis: Tables to visualize in PowerBI

CREATE SCHEMA raw;
GO

CREATE SCHEMA intermediate;
GO

CREATE SCHEMA vis;
GO

-- Grant permissions

-- USER dev needs access to everything
GRANT CREATE TABLE TO dev;
GRANT ALTER ON SCHEMA::raw TO dev;
GRANT SELECT ON SCHEMA::raw TO dev;
GRANT INSERT ON SCHEMA::raw TO dev;
GRANT DELETE ON SCHEMA::raw TO dev;
GRANT UPDATE ON SCHEMA::raw TO dev;
GRANT ALTER ON SCHEMA::intermediate TO dev;
GRANT SELECT ON SCHEMA::intermediate TO dev;
GRANT INSERT ON SCHEMA::intermediate TO dev;
GRANT DELETE ON SCHEMA::intermediate TO dev;
GRANT UPDATE ON SCHEMA::intermediate TO dev;
GRANT ALTER ON SCHEMA::vis TO dev;
GRANT SELECT ON SCHEMA::vis TO dev;
GRANT INSERT ON SCHEMA::vis TO dev;
GRANT DELETE ON SCHEMA::vis TO dev;
GRANT UPDATE ON SCHEMA::vis TO dev;
GRANT CREATE VIEW TO dev;
GRANT CREATE PROCEDURE TO dev;
GRANT ALTER TO dev;

-- USER powerbi only needs SELECT at vis
GRANT SELECT ON SCHEMA::vis TO powerbi;

-- USER acwa needs full access to schema raw
GRANT CREATE TABLE TO acwa;
GRANT ALTER ON SCHEMA::raw TO acwa;
GRANT SELECT ON SCHEMA::raw TO acwa;
GRANT INSERT ON SCHEMA::raw TO acwa;
GRANT DELETE ON SCHEMA::raw TO acwa;
GRANT UPDATE ON SCHEMA::raw TO acwa;


