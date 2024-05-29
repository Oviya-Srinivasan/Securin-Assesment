def clean_cve_data(cvedata):
    cleaned_data = []  
    seen_ids = set()   
    for cve in cvedata:
    
        if 'CVE_ID' not in cve or cve['CVE_ID'] is None:
            continue 

        cve_id = cve['CVE_ID']
        if cve_id in seen_ids:
            continue 
        else:
            seen_ids.add(cve_id)
        clean_entry = {key: value for key, value in cve.items() if value is not None}
        cleaned_data.append(clean_entry)
    print("Data cleaning process completed.")
    return cleaned_data
cleaned_cve_data = clean_cve_data('cvedata.json')
