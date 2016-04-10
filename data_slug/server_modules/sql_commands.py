table_has_any = """SELECT CASE WHEN EXISTS (SELECT 1 from %s)
    THEN 'TRUE'
    ELSE 'FALSE'
    END"""
