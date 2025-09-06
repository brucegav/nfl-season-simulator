#!/usr/bin/env python3
"""
Data Explorer for NFL Historical Data

Examines the collected CSV files and provides summaries, statistics, and data quality checks.
"""

import pandas as pd
from pathlib import Path
import numpy as np
from typing import Dict


def explore_csv_file(filepath: Path) -> Dict:
    """
    Explore a single CSV file and return summary information

    Args:
        filepath: Path to CSV file

    Returns:
        Dictionary with file analysis
    """
    try:
        df = pd.read_csv(filepath)

        analysis = {
            'filename': filepath.name,
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
            'null_counts': df.isnull().sum().to_dict(),
            'sample_data': df.head(3).to_dict('records')
        }

        # Add numeric column statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            analysis['numeric_stats'] = df[numeric_cols].describe().to_dict()

        # Add categorical column info
        object_cols = df.select_dtypes(include=['object']).columns
        if len(object_cols) > 0:
            analysis['categorical_info'] = {}
            for col in object_cols:
                unique_count = df[col].nunique()
                analysis['categorical_info'][col] = {
                    'unique_values': unique_count,
                    'top_values': df[col].value_counts().head(5).to_dict()
                }

        return analysis

    except Exception as e:
        return {'filename': filepath.name, 'error': str(e)}


def explore_historical_data(data_dir: Path = None) -> Dict:
    """
    Explore all CSV files in the historical data directory

    Args:
        data_dir: Path to data directory (defaults to ./data/historical)

    Returns:
        Dictionary with analysis of all files
    """
    if data_dir is None:
        historical_dir = Path("/Users/brucegavins/nfl-season-simulator/data/historical")
    else:
        historical_dir = data_dir / "historical"

    if not historical_dir.exists():
        return {'error': f"Directory not found: {historical_dir}"}

    csv_files = list(historical_dir.glob("*.csv"))
    if not csv_files:
        return {'error': f"No CSV files found in {historical_dir}"}

    print(f"Found {len(csv_files)} CSV files in {historical_dir}")
    print("=" * 60)

    all_analyses = {}

    for csv_file in csv_files:
        print(f"\nAnalyzing: {csv_file.name}")
        print("-" * 40)

        analysis = explore_csv_file(csv_file)
        all_analyses[csv_file.name] = analysis

        if 'error' in analysis:
            print(f"ERROR: {analysis['error']}")
            continue

        # Print summary
        print(f"Shape: {analysis['shape'][0]} rows × {analysis['shape'][1]} columns")
        print(f"Memory: {analysis['memory_usage']}")

        # Show columns
        print(f"Columns ({len(analysis['columns'])}):")
        for i, col in enumerate(analysis['columns']):
            if i < 10:  # Show first 10 columns
                dtype = analysis['dtypes'][col]
                null_count = analysis['null_counts'][col]
                print(f"  {col} ({dtype}) - {null_count} nulls")
            elif i == 10:
                print(f"  ... and {len(analysis['columns']) - 10} more columns")
                break

        # Show sample data
        print("Sample data (first 2 rows):")
        if 'sample_data' in analysis and analysis['sample_data']:
            for i, row in enumerate(analysis['sample_data'][:2]):
                print(f"  Row {i + 1}: {dict(list(row.items())[:5])}...")  # Show first 5 fields

        print()

    return all_analyses


def quick_data_check():
    """Quick data quality checks on the collected files"""

    data_dir = Path("/Users/brucegavins/nfl-season-simulator/data/historical/")

    print("Quick Data Quality Check")
    print("=" * 50)

    # Expected files
    expected_files = [
        'game_results_',
        'season_stats_',
        'player_stats_seasonal_',
        'team_descriptions_'
    ]

    csv_files = list(data_dir.glob("*.csv"))

    print(f"Files found: {len(csv_files)}")
    for f in csv_files:
        print(f"  - {f.name}")

    print("\nFile-specific checks:")
    print("-" * 30)

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        print(f"\n{csv_file.name}:")

        if 'game_results' in csv_file.name:
            print(f"  Games: {len(df)} total")
            if 'season' in df.columns:
                print(f"  Seasons: {df['season'].min()} to {df['season'].max()}")
            if 'week' in df.columns:
                print(f"  Weeks: {df['week'].min()} to {df['week'].max()}")

        elif 'player_stats' in csv_file.name:
            print(f"  Player records: {len(df)}")
            if 'season' in df.columns:
                print(f"  Seasons: {df['season'].min()} to {df['season'].max()}")
            if 'player_name' in df.columns:
                print(f"  Unique players: {df['player_name'].nunique()}")

        elif 'season_stats' in csv_file.name:
            print(f"  Team-season records: {len(df)}")
            if 'recent_team' in df.columns:
                print(f"  Teams: {df['recent_team'].nunique()}")
            if 'season' in df.columns:
                print(f"  Seasons: {df['season'].min()} to {df['season'].max()}")

        elif 'team_descriptions' in csv_file.name:
            print(f"  Team records: {len(df)}")
            if 'team_abbr' in df.columns:
                print(f"  Teams: {', '.join(df['team_abbr'].head(10).tolist())}")


def examine_specific_file(filename: str, rows: int = 10):
    """
    Examine a specific file in detail

    Args:
        filename: Name of CSV file to examine
        rows: Number of rows to display
    """
    filepath = Path("data/historical") / filename

    if not filepath.exists():
        print(f"File not found: {filepath}")
        return

    print(f"Detailed examination of: {filename}")
    print("=" * 60)

    df = pd.read_csv(filepath)

    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print()

    print("Data types:")
    print(df.dtypes)
    print()

    print("Null value counts:")
    print(df.isnull().sum())
    print()

    print(f"First {rows} rows:")
    print(df.head(rows))
    print()

    # Show unique values for key columns
    key_columns = ['season', 'week', 'team', 'recent_team', 'player_name', 'position']
    for col in key_columns:
        if col in df.columns:
            unique_count = df[col].nunique()
            print(f"{col}: {unique_count} unique values")
            if unique_count < 50:
                print(f"  Values: {sorted(df[col].unique())}")
            else:
                print(f"  Sample: {list(df[col].unique()[:10])}")


if __name__ == "__main__":
    # Run quick data check
    #quick_data_check()

    # Uncomment to run full exploration
    explore_historical_data()

    # Uncomment to examine specific file
    # examine_specific_file("game_results_2019-2023.csv")