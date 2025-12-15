#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified database initialization script
Calls both database.py and database_extended.py in the correct order
"""

if __name__ == '__main__':
    print("📊 Initializing complete database...")
    print()

    # Initialize base database
    print("Step 1/2: Creating base tables (saints, holidays, name_days, events)")
    from database import init_db
    init_db()

    print()
    print("Step 2/2: Adding extended features (proverbs, recipes, agricultural tips)")
    from database_extended import extend_database
    extend_database()

    print()
    print("=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print()
    print("Database includes:")
    print("  • 27+ Santi with biographies")
    print("  • 25+ Festività (nazionali e regionali)")
    print("  • 100+ Onomastici")
    print("  • 30+ Proverbi tradizionali")
    print("  • 9 Ricette stagionali")
    print("  • 24+ Consigli agricoli")
    print("  • 10+ Eventi storici")
    print()
    print("Total: 200+ entries ready to use!")
    print()
