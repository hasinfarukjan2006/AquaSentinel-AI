import os
import pandas as pd

def normalize_geography():
    derived_dir = 'data/derived'
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    mappings = []

    # 1. Standard State Mappings dictionary
    state_aliases = {
        'ANDHRA PRADESH': 'Andhra Pradesh',
        'andhra pradesh': 'Andhra Pradesh',
        'ARUNACHAL PRADESH': 'Arunachal Pradesh',
        'arunachal pradesh': 'Arunachal Pradesh',
        'ASSAM': 'Assam',
        'assam': 'Assam',
        'TAMIL NADU': 'Tamil Nadu',
        'tamil nadu': 'Tamil Nadu',
        'Tamil nadu': 'Tamil Nadu',
        'KERALA': 'Kerala',
        'kerala': 'Kerala',
        'KARNATAKA': 'Karnataka',
        'karnataka': 'Karnataka',
        'MAHARASHTRA': 'Maharashtra',
        'maharashtra': 'Maharashtra',
        'GUJARAT': 'Gujarat',
        'gujarat': 'Gujarat',
        'ODISHA': 'Odisha',
        'odisha': 'Odisha',
        'WEST BENGAL': 'West Bengal',
        'west bengal': 'West Bengal'
    }

    # 2. Inspect Water Quality derived file for states & districts
    wq_clean_path = os.path.join(derived_dir, 'cleaned_water_quality.csv')
    if os.path.exists(wq_clean_path):
        df_wq = pd.read_csv(wq_clean_path)
        
        # Unique state, district pairs
        pairs = df_wq[['State_UT', 'District']].drop_duplicates().values
        
        for state_raw, dist_raw in pairs:
            if pd.isna(state_raw) or str(state_raw).strip() == '':
                continue
            
            state_clean = str(state_raw).strip()
            state_canonical = state_aliases.get(state_clean, state_clean.title())
            
            if pd.isna(dist_raw) or str(dist_raw).strip() == '':
                dist_canonical = "UNKNOWN"
                match_method = "FALLBACK"
                confidence = 0.0
                review_req = True
                status = "UNMATCHED"
            else:
                dist_clean = str(dist_raw).strip()
                # Remove common suffixes
                dist_sub = dist_clean.replace(" District", "").replace(" Dist.", "").replace(" district", "").strip()
                dist_canonical = dist_sub.title()
                
                if dist_clean.lower() == dist_canonical.lower():
                    match_method = "EXACT_NORMALIZED"
                    confidence = 1.0
                    review_req = False
                    status = "MATCHED"
                else:
                    match_method = "SUFFIX_REMOVAL"
                    confidence = 0.95
                    review_req = False
                    status = "MATCHED"
            
            mappings.append({
                'source_name': dist_raw,
                'canonical_name': dist_canonical,
                'state': state_canonical,
                'match_method': match_method,
                'confidence': confidence,
                'review_required': review_req,
                'match_status': status
            })

    # Save to geography_mapping.csv
    df_map = pd.DataFrame(mappings).drop_duplicates(subset=['source_name', 'state'])
    map_csv_path = os.path.join(processed_dir, 'geography_mapping.csv')
    df_map.to_csv(map_csv_path, index=False)
    print(f"Geography normalization complete. Created {len(df_map)} geographic mappings in:\n  - {map_csv_path}")

if __name__ == '__main__':
    normalize_geography()
