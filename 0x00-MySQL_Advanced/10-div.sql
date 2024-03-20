-- Write a SQL script that creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0.
--
-- Requirements:
--
-- You must create a function
-- The function SafeDiv takes 2 arguments:
-- a, INT
-- b, INT
-- And returns a / b or 0 if b == 0

CREATE FUNCTION SafeDiv (@a INT, @b INT)
RETURNS INT
AS
BEGIN
    IF @b = 0
        RETURN 0;
    ELSE
        RETURN @a / @b;
END;
