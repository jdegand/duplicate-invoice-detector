import pandas as pd
import os

def run_audit():
    input_file = os.path.join('data', 'mock_corporate_ledger.csv')
    output_dir = 'outputs'
    output_file = os.path.join(output_dir, 'audited_corporate_ledger.csv')
    
    if not os.path.exists(input_file):
        print(f"Error: Could not find base data file at {input_file}")
        return

    # Ensure output directory exists dynamically
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load and clean types
    df = pd.read_csv(input_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(by=['Employee_ID', 'Timestamp']).reset_index(drop=True)

    df['Audit_Flag'] = 'Clear'
    df['Audit_Notes'] = ''

    # Define standard merchant category mapping for Control 5
    mismatches = {
        'Uber': 'Ground Transit',
        'Delta Air Lines': 'Travel',
        'Marriott Hotels': 'Lodging',
        'Staples': 'Office Supplies',
        'Amazon Business': 'Office Supplies'
    }

    # Evaluate rows for standard financial anomalies
    for i in range(len(df)):
        current_row = df.iloc[i]
        notes = []
        
        # --- 1. Single Row Internal Policy Controls ---
        # Control 3: Weekend Policy Violations (5 = Saturday, 6 = Sunday)
        if current_row['Timestamp'].weekday() in [5,6]:
            df.at[i, 'Audit_Flag'] = 'WARNING'
            notes.append("Weekend transaction.")
            
        # Control 4: Round-Number Padding Flag
        if current_row['Amount'] % 1 == 0 and current_row['Amount'] >= 50:
            df.at[i, 'Audit_Flag'] = 'WARNING'
            notes.append("Even round-number expense (>= $50).")

        # Control 5: Vendor Category Mismatch Detection
        merchant = current_row['Merchant']
        if merchant in mismatches and current_row['Category'] != mismatches[merchant]:
            df.at[i, 'Audit_Flag'] = 'WARNING'
            notes.append(f"Category mismatch: Expected '{mismatches[merchant]}'.")

        # Combine any individual single-row violation messages
        if notes:
            df.at[i, 'Audit_Notes'] = " | ".join(notes)

        # --- 2. Relational Checks (Cross-Row Evaluation - Can override single row flags) ---
        for j in range(len(df)):
            if i == j:
                continue
            compare_row = df.iloc[j]
            time_diff = abs((current_row['Timestamp'] - compare_row['Timestamp']).total_seconds() / 60.0)
            
            # CONTROL 1: Exact Duplicate (Different Employee)
            if (current_row['Merchant'] == compare_row['Merchant'] and 
                current_row['Amount'] == compare_row['Amount'] and 
                current_row['Timestamp'].date() == compare_row['Timestamp'].date() and 
                current_row['Employee_ID'] != compare_row['Employee_ID']):
                
                df.at[i, 'Audit_Flag'] = 'CRITICAL'
                df.at[i, 'Audit_Notes'] = f"Potential fraud/double-billing. Matches {compare_row['Transaction_ID']} ({compare_row['Employee_ID']})."
                break

            # CONTROL 2: Potential Split Transaction / Multi-Swipe (Same Employee)
            elif (current_row['Employee_ID'] == compare_row['Employee_ID'] and 
                  current_row['Merchant'] == compare_row['Merchant'] and 
                  current_row['Amount'] == compare_row['Amount'] and 
                  time_diff <= 15.0):
                  
                  df.at[i, 'Audit_Flag'] = 'WARNING'
                  if current_row['Amount'] >= 500:
                      df.at[i, 'Audit_Notes'] = f"Corporate Limit Threshold Bypass. Split charge with {compare_row['Transaction_ID']}."
                  else:
                      df.at[i, 'Audit_Notes'] = f"Potential double-swipe. Within {int(time_diff)} mins of {compare_row['Transaction_ID']}."
                  break

    # Format output for clean visualization
    df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    df['Amount'] = df['Amount'].map('{:,.2f}'.format)
    
    df.to_csv(output_file, index=False)
    print(f"Audit successfully exported to -> {output_file}")

if __name__ == "__main__":
    run_audit()
