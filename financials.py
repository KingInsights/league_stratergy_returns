import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# Intelligent, cheeky intro banner
# =============================
st.title("⚽ Football League Financial Returns Analysis")
st.markdown("""
### 🎯 Welcome to the Data Playground — real results, no sugarcoating.  
We’ve scraped match data from a selection of leagues and feature-engineered it to calculate running season returns from a generous mix of intelligent, thought-provoking betting strategies:  
£10 on every home win, away win, draw, favourite (lowest odds), second favourite, Le Underdog (highest odds), and even a random pick.  
All crunched, all laid bare — showing how those choices would have fared over an entire season.
""")

st.write("Select leagues and load data — then choose what to view.")

# =============================
# League file paths
# =============================
league_files = {
    "Premier League": "england_premier-league-2023-2024_financial_returns.csv",
    "Championship": "england_championship-2023-2024_financial_returns.csv",
    "League Two": "england_league-two-2023-2024_financial_returns.csv",
    "League One": "england_league-one-2023-2024_financial_returns.csv",
    "Serie A (Italy)": "italy_serie-a-2023-2024_financial_returns.csv",
    "La Liga (Spain)": "spain_laliga-2023-2024_financial_returns.csv",
    "Liga Portugal": "portugal_liga-portugal-2023-2024_financial_returns.csv",
    "Ligue 1 (France)": "france_ligue-1-2023-2024_financial_returns.csv",
    "Ekstraklasa (Poland)": "poland_ekstraklasa-2023-2024_financial_returns.csv"
}

# =============================
# Color + Description Maps
# =============================
strategy_colors = {
    'home_returns_running_total': 'blue',
    'draw_returns_running_total': 'orange',
    'away_returns_running_total': 'green',
    'first_choice_returns_running_total': 'purple',
    'second_choice_returns_running_total': 'red',
    'third_choice_returns_running_total': 'brown',
    'random_choice_1_running_balance': 'magenta'
}

label_dict = {
    'home_returns_running_total': "£10 bet on every home win",
    'draw_returns_running_total': "£10 bet on every draw",
    'away_returns_running_total': "£10 bet on every away win",
    'first_choice_returns_running_total': "£10 on the favourite (lowest odds)",
    'second_choice_returns_running_total': "£10 on second favourite",
    'third_choice_returns_running_total': "£10 on Le Underdog (highest odds)",
    'random_choice_1_running_balance': "£10 random pick simulation"
}

# Column name mapping for summary best/worst columns:
column_name_map = {
    'home_returns_total': "£10 bet on every home win",
    'draw_returns_total': "£10 bet on every draw",
    'away_returns_total': "£10 bet on every away win",
    'first_choice_returns_total': "£10 on the favourite (lowest odds)",
    'second_choice_returns_total': "£10 on second favourite",
    'third_choice_returns_total': "£10 on Le Underdog (highest odds)",
    'random_choice_1_total': "£10 random pick simulation"
}

# =============================
# League selection and loading
# =============================
selected_leagues = st.multiselect("Select League(s) to Load", list(league_files.keys()))

if st.button("Load Data"):
    if not selected_leagues:
        st.warning("Please select at least one league.")
    else:
        st.info("✅ Scraped with intelligent imagination — fun, free, and powered by Selenium.")
        for league in selected_leagues:
            file_path = league_files[league]
            df = pd.read_csv(file_path)

            season = file_path.split('-')[-2] + '-' + file_path.split('-')[-1].replace('_financial_returns.csv', '')
            df.insert(0, "league_name", league)
            df.insert(1, "season", season)

            st.session_state[f"{league}_df"] = df

        st.success("✅ Data loaded! Now choose what you’d like to view.")

# =============================
# Fixture-by-fixture plots
# =============================
if st.button("View Financial Return Columns Plots"):
    st.caption("✅ Visual test: Watching strategies rise, sink, or wobble around.")
    for league in selected_leagues:
        key_name = f"{league}_df"
        if key_name in st.session_state:
            df = st.session_state[key_name]
            cols_to_plot = list(strategy_colors.keys())

            st.write(f"## {league} ({df.iloc[0]['season']}) — Fixture-by-Fixture Returns")
            fig, ax = plt.subplots(figsize=(14, 6))

            ymax = df[cols_to_plot].max().max()
            ymin = df[cols_to_plot].min().min()
            ax.axhspan(0, ymax, facecolor='lightgreen', alpha=0.3)
            ax.axhspan(ymin, 0, facecolor='mistyrose', alpha=0.4)

            for col in cols_to_plot:
                ax.plot(df.index, df[col], label=col, color=strategy_colors[col], linewidth=2)

            ax.axhline(0, color='black', linestyle='--', linewidth=2)
            ax.set_xlim(0, len(df) - 1)
            ax.set_xlabel('Fixture Number', fontsize=13)
            ax.set_ylabel('Running Returns (£)', fontsize=13)
            ax.set_title(f"{league} — {df.iloc[0]['season']}", fontsize=16)
            ax.grid(True)
            st.pyplot(fig)

            st.markdown("---")
            st.write("### Strategy Key:")
            for col in cols_to_plot:
                color = strategy_colors[col]
                description = label_dict[col]
                st.markdown(
                    f"<div style='display: flex; align-items: center; margin-bottom: 8px;'>"
                    f"<div style='width: 20px; height: 20px; background-color: {color}; "
                    f"margin-right: 10px; border: 1px solid #000;'></div>"
                    f"<span style='font-size:16px;'>{description}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            st.markdown("---")

# =============================
# Best & worst return analysis
# =============================
if st.button("View Combined Best & Worst Returns"):
    st.caption("✅ Crunch test: Let’s see who strutted and who stumbled, league by league.")
    best_worst_records = []

    for league in selected_leagues:
        key_name = f"{league}_df"
        if key_name in st.session_state:
            df = st.session_state[key_name]
            final_values = {col.replace('_running_total', '_total').replace('_running_balance', '_total'): df[col].iloc[-1] for col in strategy_colors.keys()}
            best_col = max(final_values, key=final_values.get)
            worst_col = min(final_values, key=final_values.get)

            best_worst_records.append({
                'league_name': league,
                'best_return': final_values[best_col],
                'best_return_column': best_col,
                'worst_return': final_values[worst_col],
                'worst_return_column': worst_col
            })

    summary_df = pd.DataFrame(best_worst_records)

    # Add descriptive names
    summary_df['best_return_column_desc'] = summary_df['best_return_column'].map(column_name_map)
    summary_df['worst_return_column_desc'] = summary_df['worst_return_column'].map(column_name_map)

    # Reorder columns for clean display
    summary_df_display = summary_df[['league_name', 'best_return', 'best_return_column_desc', 'worst_return', 'worst_return_column_desc']]
    summary_df_display['best_return'] = summary_df_display['best_return'].apply(lambda x: f"£{x:,.2f}")
    summary_df_display['worst_return'] = summary_df_display['worst_return'].apply(lambda x: f"£{x:,.2f}")

    st.write("### Best & Worst Returns (From Current Loaded Leagues)")
    st.dataframe(summary_df_display)

    # Plot best returns
    st.write("### ✅ Best Return Per League")
    best_colors = summary_df['best_return_column'].map(lambda x: strategy_colors.get(x.replace('_total', '_running_total'), 'grey'))
    fig_best, ax_best = plt.subplots(figsize=(12, 6))
    ax_best.bar(summary_df['league_name'], summary_df['best_return'], color=best_colors)
    ax_best.set_ylabel("Best Return (£)", fontsize=12)
    ax_best.set_xticklabels(summary_df['league_name'], rotation=45, ha='right')
    ax_best.set_title("Best Strategy Return Per League (Selected Leagues)", fontsize=14)
    ax_best.axhline(0, color='black', linestyle='--')
    st.pyplot(fig_best)

    st.write("### Strategy Key:")
    for col, desc in column_name_map.items():
        color = strategy_colors.get(col.replace('_total', '_running_total'), 'grey')
        st.markdown(
            f"<div style='display: flex; align-items: center; margin-bottom: 8px;'>"
            f"<div style='width: 20px; height: 20px; background-color: {color}; "
            f"margin-right: 10px; border: 1px solid #000;'></div>"
            f"<span style='font-size:16px;'>{desc}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Plot worst returns
    st.write("### ❌ Worst Return Per League")
    worst_colors = summary_df['worst_return_column'].map(lambda x: strategy_colors.get(x.replace('_total', '_running_total'), 'grey'))
    fig_worst, ax_worst = plt.subplots(figsize=(12, 6))
    ax_worst.bar(summary_df['league_name'], summary_df['worst_return'], color=worst_colors)
    ax_worst.set_ylabel("Worst Return (£)", fontsize=12)
    ax_worst.set_xticklabels(summary_df['league_name'], rotation=45, ha='right')
    ax_worst.set_title("Worst Strategy Return Per League (Selected Leagues)", fontsize=14)
    ax_worst.axhline(0, color='black', linestyle='--')
    st.pyplot(fig_worst)

    st.write("### Strategy Key:")
    for col, desc in column_name_map.items():
        color = strategy_colors.get(col.replace('_total', '_running_total'), 'grey')
        st.markdown(
            f"<div style='display: flex; align-items: center; margin-bottom: 8px;'>"
            f"<div style='width: 20px; height: 20px; background-color: {color}; "
            f"margin-right: 10px; border: 1px solid #000;'></div>"
            f"<span style='font-size:16px;'>{desc}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

# ✅ Closing line
st.markdown("**Play with it, spot the patterns — and see who really comes out on top. Definitely food for thought.**")
st.markdown("*Built by someone who’s been there, fallen, got up again, fallen once more — and now... drinking beers, crunching peanuts and numbers.* 🍻")
