-- Fixture: ensure tb_countries has known reference data.
-- The main tb_countries.sql in files/ inserts ~250 countries.
-- This fixture only verifies a few known rows exist for test assertions.
--
-- If running against a fresh database, execute files/tb_countries.sql first,
-- then this fixture is optional (the full dataset already includes these).

-- Verify these countries exist (safe re-insert with existence check)
IF NOT EXISTS (SELECT 1 FROM tb_countries WHERE code = 'US')
  INSERT INTO tb_countries (name, code, currency, population, capital)
  VALUES ('United States', 'US', 'USD', '310232863', 'Washington');

IF NOT EXISTS (SELECT 1 FROM tb_countries WHERE code = 'KR')
  INSERT INTO tb_countries (name, code, currency, population, capital)
  VALUES ('South Korea', 'KR', 'KRW', '48422644', 'Seoul');

IF NOT EXISTS (SELECT 1 FROM tb_countries WHERE code = 'JP')
  INSERT INTO tb_countries (name, code, currency, population, capital)
  VALUES ('Japan', 'JP', 'JPY', '127288000', 'Tokyo');
