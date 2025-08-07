"""
Constants and Static Data for BullBoard Application
Contains CSS styling, symbol mappings, and UI constants
"""

# ==========================================
# CSS STYLING
# ==========================================
CUSTOM_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced Header Styling */
   .main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="20" cy="80" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    pointer-events: none;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.logo-icon {
    font-size: 3.5rem;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}

.logo-text h1 {
    margin: 0;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(45deg, #ffffff, #f8f9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.tagline {
    font-size: 1.2rem;
    font-weight: 500;
    opacity: 0.95;
    margin-top: 0.25rem;
}

.value-props {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}

.prop-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: transform 0.3s ease;
}

.prop-item:hover {
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.2);
}

.prop-icon {
    font-size: 1.8rem;
}

.prop-text {
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    white-space: nowrap;
}

.header-subtitle {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 1rem;
    opacity: 0.9;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1.5rem;
        text-align: center;
    }
    
    .value-props {
        justify-content: center;
        gap: 1rem;
    }
    
    .logo-text h1 {
        font-size: 2.5rem;
    }
    
    .tagline {
        font-size: 1rem;
    }
}
    
/* Metric Cards - Fixed height and text positioning */
.metric-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 50%, #ffffff 100%);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 
        0 4px 6px -1px rgba(0, 0, 0, 0.1),
        0 2px 4px -1px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    height: 160px; /* Increased from 140px */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: 8px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 
        0 12px 25px rgba(102, 126, 234, 0.15),
        0 8px 10px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    border-color: rgba(102, 126, 234, 0.3);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-radius: 0 2px 2px 0;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100px;
    height: 100px;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
    border-radius: 50%;
}

.metric-header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.metric-icon {
    font-size: 18px;
    margin-right: 10px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.metric-title {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    line-height: 1.2 !important;
}

.metric-value {
    font-size: 28px !important; /* Slightly smaller to make room */
    font-weight: 800 !important;
    color: #1e293b !important;
    margin: 8px 0 12px 0 !important; /* Added bottom margin */
    line-height: 1.1 !important;
    position: relative;
    z-index: 1;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.metric-subtitle {
    font-size: 13px !important; /* Slightly smaller but still readable */
    color: #667eea !important;
    font-weight: 600 !important;
    position: relative;
    z-index: 1;
    text-transform: capitalize;
    line-height: 1.2 !important;
    margin-bottom: 4px !important; /* Add bottom margin */
    display: block !important; /* Ensure it displays properly */
}

/* Section Headers - Keep existing styles */
.section-header {
    display: flex;
    align-items: center;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e2e8f0;
}

.section-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.section-header h2 {
    margin: 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
}

/* Fix for dark theme text visibility */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.main .block-container {
    color: #ffffff;
}

/* Additional refinements */
.element-container {
    margin-bottom: 0 !important;
}

/* Responsive adjustments for cards */
@media (max-width: 768px) {
    .metric-card {
        height: 120px;
        padding: 16px;
    }
    
    .metric-value {
        font-size: 24px !important;
    }
    
    .metric-title {
        font-size: 10px !important;
    }
}

/* Section Headers - Fixed colors */
.section-header {
    display: flex;
    align-items: center;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e2e8f0;
}

.section-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.section-header h2 {
    margin: 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
}

/* Fix for dark theme text visibility */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.main .block-container {
    color: #ffffff;
}
    
    /* Status Cards */
    .status-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .status-success {
        background: #d5f4e6;
        border-color: #2ecc71;
        color: #27ae60;
    }
    
    .status-warning {
        background: #fef9e7;
        border-color: #f39c12;
        color: #e67e22;
    }
    
    .status-info {
        background: #ebf3fd;
        border-color: #3498db;
        color: #2980b9;
    }
    
    /* AI Insight Cards */
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffd700;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }
    
    .section-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# ==========================================
# STOCK SYMBOL MAPPINGS  
# ==========================================
SYMBOL_TO_NAME_MAPPING = {
        # A
        'A': 'Agilent Technologies Inc.',
        'AAL': 'American Airlines Group Inc.',
        'AAP': 'Advance Auto Parts Inc.',
        'AAPL': 'Apple Inc.',
        'ABBV': 'AbbVie Inc.',
        'ABC': 'AmerisourceBergen Corp.',
        'ABMD': 'Abiomed Inc.',
        'ABT': 'Abbott Laboratories',
        'ACN': 'Accenture PLC',
        'ADBE': 'Adobe Inc.',
        'ADI': 'Analog Devices Inc.',
        'ADM': 'Archer-Daniels-Midland Co.',
        'ADP': 'Automatic Data Processing Inc.',
        'ADSK': 'Autodesk Inc.',
        'AEE': 'Ameren Corp.',
        'AEP': 'American Electric Power Co. Inc.',
        'AES': 'AES Corp.',
        'AFL': 'Aflac Inc.',
        'AIG': 'American International Group Inc.',
        'AIZ': 'Assurant Inc.',
        'AJG': 'Arthur J. Gallagher & Co.',
        'AKAM': 'Akamai Technologies Inc.',
        'ALB': 'Albemarle Corp.',
        'ALGN': 'Align Technology Inc.',
        'ALK': 'Alaska Air Group Inc.',
        'ALL': 'Allstate Corp.',
        'ALLE': 'Allegion PLC',
        'AMAT': 'Applied Materials Inc.',
        'AMCR': 'Amcor PLC',
        'AMD': 'Advanced Micro Devices Inc.',
        'AME': 'AMETEK Inc.',
        'AMGN': 'Amgen Inc.',
        'AMP': 'Ameriprise Financial Inc.',
        'AMT': 'American Tower Corp.',
        'AMZN': 'Amazon.com Inc.',
        'ANET': 'Arista Networks Inc.',
        'ANSS': 'ANSYS Inc.',
        'AON': 'Aon PLC',
        'AOS': 'A.O. Smith Corp.',
        'APA': 'APA Corp.',
        'APD': 'Air Products and Chemicals Inc.',
        'APH': 'Amphenol Corp.',
        'APTV': 'Aptiv PLC',
        'ARE': 'Alexandria Real Estate Equities Inc.',
        'ATO': 'Atmos Energy Corp.',
        'ATVI': 'Activision Blizzard Inc.',
        'AVB': 'AvalonBay Communities Inc.',
        'AVGO': 'Broadcom Inc.',
        'AVY': 'Avery Dennison Corp.',
        'AWK': 'American Water Works Co. Inc.',
        'AXP': 'American Express Co.',
        'AZO': 'AutoZone Inc.',
        
        # B
        'BA': 'Boeing Co.',
        'BAC': 'Bank of America Corp.',
        'BALL': 'Ball Corp.',
        'BAX': 'Baxter International Inc.',
        'BBWI': 'Bath & Body Works Inc.',
        'BBY': 'Best Buy Co. Inc.',
        'BDX': 'Becton Dickinson and Co.',
        'BEN': 'Franklin Resources Inc.',
        'BF-B': 'Brown-Forman Corp.',
        'BIIB': 'Biogen Inc.',
        'BIO': 'Bio-Rad Laboratories Inc.',
        'BK': 'Bank of New York Mellon Corp.',
        'BKNG': 'Booking Holdings Inc.',
        'BKR': 'Baker Hughes Co.',
        'BLK': 'BlackRock Inc.',
        'BMY': 'Bristol-Myers Squibb Co.',
        'BR': 'Broadridge Financial Solutions Inc.',
        'BRK-B': 'Berkshire Hathaway Inc.',
        'BRO': 'Brown & Brown Inc.',
        'BSX': 'Boston Scientific Corp.',
        'BWA': 'BorgWarner Inc.',
        
        # C
        'C': 'Citigroup Inc.',
        'CAG': 'Conagra Brands Inc.',
        'CAH': 'Cardinal Health Inc.',
        'CARR': 'Carrier Global Corp.',
        'CAT': 'Caterpillar Inc.',
        'CB': 'Chubb Ltd.',
        'CBOE': 'Cboe Global Markets Inc.',
        'CBRE': 'CBRE Group Inc.',
        'CCI': 'Crown Castle Inc.',
        'CCL': 'Carnival Corp.',
        'CDAY': 'Ceridian HCM Holding Inc.',
        'CDNS': 'Cadence Design Systems Inc.',
        'CDW': 'CDW Corp.',
        'CE': 'Celanese Corp.',
        'CEG': 'Constellation Energy Corp.',
        'CHTR': 'Charter Communications Inc.',
        'CI': 'Cigna Corp.',
        'CINF': 'Cincinnati Financial Corp.',
        'CL': 'Colgate-Palmolive Co.',
        'CLX': 'Clorox Co.',
        'CMA': 'Comerica Inc.',
        'CMCSA': 'Comcast Corp.',
        'CME': 'CME Group Inc.',
        'CMG': 'Chipotle Mexican Grill Inc.',
        'CMI': 'Cummins Inc.',
        'CMS': 'CMS Energy Corp.',
        'CNC': 'Centene Corp.',
        'CNP': 'CenterPoint Energy Inc.',
        'COF': 'Capital One Financial Corp.',
        'COO': 'Cooper Cos. Inc.',
        'COP': 'ConocoPhillips',
        'COST': 'Costco Wholesale Corp.',
        'CPB': 'Campbell Soup Co.',
        'CPRT': 'Copart Inc.',
        'CRM': 'Salesforce Inc.',
        'CSCO': 'Cisco Systems Inc.',
        'CSX': 'CSX Corp.',
        'CTAS': 'Cintas Corp.',
        'CTLT': 'Catalent Inc.',
        'CTRA': 'Coterra Energy Inc.',
        'CTSH': 'Cognizant Technology Solutions Corp.',
        'CTVA': 'Corteva Inc.',
        'CVS': 'CVS Health Corp.',
        'CVX': 'Chevron Corp.',
        'CZR': 'Caesars Entertainment Inc.',
        
        # D
        'D': 'Dominion Energy Inc.',
        'DAL': 'Delta Air Lines Inc.',
        'DD': 'DuPont de Nemours Inc.',
        'DE': 'Deere & Co.',
        'DFS': 'Discover Financial Services',
        'DG': 'Dollar General Corp.',
        'DGX': 'Quest Diagnostics Inc.',
        'DHI': 'D.R. Horton Inc.',
        'DHR': 'Danaher Corp.',
        'DIS': 'Walt Disney Co.',
        'DISH': 'DISH Network Corp.',
        'DLR': 'Digital Realty Trust Inc.',
        'DLTR': 'Dollar Tree Inc.',
        'DOV': 'Dover Corp.',
        'DOW': 'Dow Inc.',
        'DPZ': 'Domino\'s Pizza Inc.',
        'DRE': 'Duke Realty Corp.',
        'DRI': 'Darden Restaurants Inc.',
        'DTE': 'DTE Energy Co.',
        'DUK': 'Duke Energy Corp.',
        'DVA': 'DaVita Inc.',
        'DVN': 'Devon Energy Corp.',
        
        # E
        'EA': 'Electronic Arts Inc.',
        'EBAY': 'eBay Inc.',
        'ECL': 'Ecolab Inc.',
        'ED': 'Consolidated Edison Inc.',
        'EFX': 'Equifax Inc.',
        'EIX': 'Edison International',
        'EL': 'Estee Lauder Cos. Inc.',
        'EMN': 'Eastman Chemical Co.',
        'EMR': 'Emerson Electric Co.',
        'ENPH': 'Enphase Energy Inc.',
        'EOG': 'EOG Resources Inc.',
        'EPAM': 'EPAM Systems Inc.',
        'EQIX': 'Equinix Inc.',
        'EQR': 'Equity Residential',
        'ES': 'Eversource Energy',
        'ESS': 'Essex Property Trust Inc.',
        'ETN': 'Eaton Corp. PLC',
        'ETR': 'Entergy Corp.',
        'ETSY': 'Etsy Inc.',
        'EVRG': 'Evergy Inc.',
        'EW': 'Edwards Lifesciences Corp.',
        'EXC': 'Exelon Corp.',
        'EXPD': 'Expeditors International of Washington Inc.',
        'EXPE': 'Expedia Group Inc.',
        'EXR': 'Extended Stay America Inc.',
        
        # F
        'F': 'Ford Motor Co.',
        'FANG': 'Diamondback Energy Inc.',
        'FAST': 'Fastenal Co.',
        'FBHS': 'Fortune Brands Home & Security Inc.',
        'FCX': 'Freeport-McMoRan Inc.',
        'FDS': 'FactSet Research Systems Inc.',
        'FDX': 'FedEx Corp.',
        'FE': 'FirstEnergy Corp.',
        'FFIV': 'F5 Inc.',
        'FIS': 'Fidelity National Information Services Inc.',
        'FISV': 'Fiserv Inc.',
        'FITB': 'Fifth Third Bancorp',
        'FLT': 'FleetCor Technologies Inc.',
        'FMC': 'FMC Corp.',
        'FOX': 'Fox Corp.',
        'FOXA': 'Fox Corp.',
        'FRC': 'First Republic Bank',
        'FRT': 'Federal Realty Investment Trust',
        'FTNT': 'Fortinet Inc.',
        'FTV': 'Fortive Corp.',
        
        # G
        'GD': 'General Dynamics Corp.',
        'GE': 'General Electric Co.',
        'GILD': 'Gilead Sciences Inc.',
        'GIS': 'General Mills Inc.',
        'GL': 'Globe Life Inc.',
        'GLW': 'Corning Inc.',
        'GM': 'General Motors Co.',
        'GNRC': 'Generac Holdings Inc.',
        'GOOG': 'Alphabet Inc.',
        'GOOGL': 'Alphabet Inc.',
        'GPC': 'Genuine Parts Co.',
        'GPN': 'Global Payments Inc.',
        'GRMN': 'Garmin Ltd.',
        'GS': 'Goldman Sachs Group Inc.',
        'GWW': 'W.W. Grainger Inc.',
        
        # H
        'HAL': 'Halliburton Co.',
        'HAS': 'Hasbro Inc.',
        'HBAN': 'Huntington Bancshares Inc.',
        'HBI': 'Hanesbrands Inc.',
        'HCA': 'HCA Healthcare Inc.',
        'HD': 'Home Depot Inc.',
        'HES': 'Hess Corp.',
        'HIG': 'Hartford Financial Services Group Inc.',
        'HII': 'Huntington Ingalls Industries Inc.',
        'HLT': 'Hilton Worldwide Holdings Inc.',
        'HOLX': 'Hologic Inc.',
        'HON': 'Honeywell International Inc.',
        'HPE': 'Hewlett Packard Enterprise Co.',
        'HPQ': 'HP Inc.',
        'HRL': 'Hormel Foods Corp.',
        'HSIC': 'Henry Schein Inc.',
        'HST': 'Host Hotels & Resorts Inc.',
        'HSY': 'Hershey Co.',
        'HUM': 'Humana Inc.',
        'HWM': 'Howmet Aerospace Inc.',
        
        # I
        'IBM': 'International Business Machines Corp.',
        'ICE': 'Intercontinental Exchange Inc.',
        'IDXX': 'IDEXX Laboratories Inc.',
        'IEX': 'IDEX Corp.',
        'IFF': 'International Flavors & Fragrances Inc.',
        'ILMN': 'Illumina Inc.',
        'INCY': 'Incyte Corp.',
        'INFO': 'IHS Markit Ltd.',
        'INTC': 'Intel Corp.',
        'INTU': 'Intuit Inc.',
        'IP': 'International Paper Co.',
        'IPG': 'Interpublic Group of Cos. Inc.',
        'IPGP': 'IPG Photonics Corp.',
        'IQV': 'IQVIA Holdings Inc.',
        'IR': 'Ingersoll Rand Inc.',
        'IRM': 'Iron Mountain Inc.',
        'ISRG': 'Intuitive Surgical Inc.',
        'IT': 'Gartner Inc.',
        'ITW': 'Illinois Tool Works Inc.',
        'IVZ': 'Invesco Ltd.',
        
        # J
        'JBHT': 'J.B. Hunt Transport Services Inc.',
        'JCI': 'Johnson Controls International PLC',
        'JKHY': 'Jack Henry & Associates Inc.',
        'JNJ': 'Johnson & Johnson',
        'JNPR': 'Juniper Networks Inc.',
        'JPM': 'JPMorgan Chase & Co.',
        'JWN': 'Nordstrom Inc.',
        
        # K
        'K': 'Kellogg Co.',
        'KEY': 'KeyCorp',
        'KEYS': 'Keysight Technologies Inc.',
        'KHC': 'Kraft Heinz Co.',
        'KIM': 'Kimco Realty Corp.',
        'KLAC': 'KLA Corp.',
        'KMB': 'Kimberly-Clark Corp.',
        'KMI': 'Kinder Morgan Inc.',
        'KMX': 'CarMax Inc.',
        'KO': 'Coca-Cola Co.',
        'KR': 'Kroger Co.',
        'KSS': 'Kohl\'s Corp.',
        
        # L
        'L': 'Loews Corp.',
        'LDOS': 'Leidos Holdings Inc.',
        'LEG': 'Leggett & Platt Inc.',
        'LEN': 'Lennar Corp.',
        'LH': 'Laboratory Corp. of America Holdings',
        'LHX': 'L3Harris Technologies Inc.',
        'LIN': 'Linde PLC',
        'LKQ': 'LKQ Corp.',
        'LLY': 'Eli Lilly and Co.',
        'LMT': 'Lockheed Martin Corp.',
        'LNC': 'Lincoln National Corp.',
        'LNT': 'Alliant Energy Corp.',
        'LOW': 'Lowe\'s Cos. Inc.',
        'LRCX': 'Lam Research Corp.',
        'LUMN': 'Lumen Technologies Inc.',
        'LUV': 'Southwest Airlines Co.',
        'LVS': 'Las Vegas Sands Corp.',
        'LW': 'Lamb Weston Holdings Inc.',
        'LYB': 'LyondellBasell Industries NV',
        'LYV': 'Live Nation Entertainment Inc.',
        
        # M
        'MA': 'Mastercard Inc.',
        'MAA': 'Mid-America Apartment Communities Inc.',
        'MAR': 'Marriott International Inc.',
        'MAS': 'Masco Corp.',
        'MCD': 'McDonald\'s Corp.',
        'MCHP': 'Microchip Technology Inc.',
        'MCK': 'McKesson Corp.',
        'MCO': 'Moody\'s Corp.',
        'MDLZ': 'Mondelez International Inc.',
        'MDT': 'Medtronic PLC',
        'MET': 'MetLife Inc.',
        'META': 'Meta Platforms Inc.',
        'MGM': 'MGM Resorts International',
        'MHK': 'Mohawk Industries Inc.',
        'MKC': 'McCormick & Co. Inc.',
        'MKTX': 'MarketAxess Holdings Inc.',
        'MLM': 'Martin Marietta Materials Inc.',
        'MMC': 'Marsh & McLennan Cos. Inc.',
        'MMM': '3M Co.',
        'MNST': 'Monster Beverage Corp.',
        'MO': 'Altria Group Inc.',
        'MOH': 'Molina Healthcare Inc.',
        'MOS': 'Mosaic Co.',
        'MPC': 'Marathon Petroleum Corp.',
        'MPWR': 'Monolithic Power Systems Inc.',
        'MRK': 'Merck & Co. Inc.',
        'MRNA': 'Moderna Inc.',
        'MRO': 'Marathon Oil Corp.',
        'MS': 'Morgan Stanley',
        'MSCI': 'MSCI Inc.',
        'MSFT': 'Microsoft Corp.',
        'MSI': 'Motorola Solutions Inc.',
        'MTB': 'M&T Bank Corp.',
        'MTCH': 'Match Group Inc.',
        'MTD': 'Mettler-Toledo International Inc.',
        'MU': 'Micron Technology Inc.',
        'NCLH': 'Norwegian Cruise Line Holdings Ltd.',
        'NDAQ': 'Nasdaq Inc.',
        'NDSN': 'Nordson Corp.',
        'NEE': 'NextEra Energy Inc.',
        'NEM': 'Newmont Corp.',
        'NFLX': 'Netflix Inc.',
        'NI': 'NiSource Inc.',
        'NKE': 'Nike Inc.',
        'NLOK': 'NortonLifeLock Inc.',
        'NLSN': 'Nielsen Holdings PLC',
        'NOC': 'Northrop Grumman Corp.',
        'NOW': 'ServiceNow Inc.',
        'NRG': 'NRG Energy Inc.',
        'NSC': 'Norfolk Southern Corp.',
        'NTAP': 'NetApp Inc.',
        'NTRS': 'Northern Trust Corp.',
        'NUE': 'Nucor Corp.',
        'NVDA': 'NVIDIA Corp.',
        'NVR': 'NVR Inc.',
        'NWL': 'Newell Brands Inc.',
        'NWS': 'News Corp.',
        'NWSA': 'News Corp.',
        
        # O
        'ODFL': 'Old Dominion Freight Line Inc.',
        'OGN': 'Organon & Co.',
        'OKE': 'ONEOK Inc.',
        'OMC': 'Omnicom Group Inc.',
        'ORCL': 'Oracle Corp.',
        'ORLY': 'O\'Reilly Automotive Inc.',
        'OTIS': 'Otis Worldwide Corp.',
        'OXY': 'Occidental Petroleum Corp.',
        
        # P
        'PARA': 'Paramount Global',
        'PAYC': 'Paycom Software Inc.',
        'PAYX': 'Paychex Inc.',
        'PCAR': 'PACCAR Inc.',
        'PCG': 'PG&E Corp.',
        'PEAK': 'Healthpeak Properties Inc.',
        'PEG': 'Public Service Enterprise Group Inc.',
        'PEP': 'PepsiCo Inc.',
        'PFE': 'Pfizer Inc.',
        'PFG': 'Principal Financial Group Inc.',
        'PG': 'Procter & Gamble Co.',
        'PGR': 'Progressive Corp.',
        'PH': 'Parker-Hannifin Corp.',
        'PHM': 'PulteGroup Inc.',
        'PKG': 'Packaging Corp. of America',
        'PKI': 'PerkinElmer Inc.',
        'PLD': 'Prologis Inc.',
        'PM': 'Philip Morris International Inc.',
        'PNC': 'PNC Financial Services Group Inc.',
        'PNR': 'Pentair PLC',
        'PNW': 'Pinnacle West Capital Corp.',
        'POOL': 'Pool Corp.',
        'PPG': 'PPG Industries Inc.',
        'PPL': 'PPL Corp.',
        'PRU': 'Prudential Financial Inc.',
        'PSA': 'Public Storage',
        'PSX': 'Phillips 66',
        'PTC': 'PTC Inc.',
        'PVH': 'PVH Corp.',
        'PWR': 'Quanta Services Inc.',
        'PXD': 'Pioneer Natural Resources Co.',
        'PYPL': 'PayPal Holdings Inc.',
        
        # Q-R
        'QCOM': 'Qualcomm Inc.',
        'QRVO': 'Qorvo Inc.',
        'RCL': 'Royal Caribbean Cruises Ltd.',
        'RE': 'Everest Re Group Ltd.',
        'REG': 'Regency Centers Corp.',
        'REGN': 'Regeneron Pharmaceuticals Inc.',
        'RF': 'Regions Financial Corp.',
        'RHI': 'Robert Half Inc.',
        'RJF': 'Raymond James Financial Inc.',
        'RL': 'Ralph Lauren Corp.',
        'RMD': 'ResMed Inc.',
        'ROK': 'Rockwell Automation Inc.',
        'ROL': 'Rollins Inc.',
        'ROP': 'Roper Technologies Inc.',
        'ROST': 'Ross Stores Inc.',
        'RSG': 'Republic Services Inc.',
        'RTX': 'Raytheon Technologies Corp.',
        
        # S
        'SBAC': 'SBA Communications Corp.',
        'SBNY': 'Signature Bank',
        'SBUX': 'Starbucks Corp.',
        'SCHW': 'Charles Schwab Corp.',
        'SEDG': 'SolarEdge Technologies Inc.',
        'SEE': 'Sealed Air Corp.',
        'SHW': 'Sherwin-Williams Co.',
        'SIVB': 'SVB Financial Group',
        'SJM': 'J.M. Smucker Co.',
        'SLB': 'Schlumberger NV',
        'SNA': 'Snap-on Inc.',
        'SNPS': 'Synopsys Inc.',
        'SO': 'Southern Co.',
        'SPG': 'Simon Property Group Inc.',
        'SPGI': 'S&P Global Inc.',
        'SRE': 'Sempra Energy',
        'STE': 'STERIS PLC',
        'STT': 'State Street Corp.',
        'STX': 'Seagate Technology Holdings PLC',
        'STZ': 'Constellation Brands Inc.',
        'SWK': 'Stanley Black & Decker Inc.',
        'SWKS': 'Skyworks Solutions Inc.',
        'SYF': 'Synchrony Financial',
        'SYK': 'Stryker Corp.',
        'SYY': 'Sysco Corp.',
        
        # T
        'T': 'AT&T Inc.',
        'TAP': 'Molson Coors Beverage Co.',
        'TDG': 'TransDigm Group Inc.',
        'TDY': 'Teledyne Technologies Inc.',
        'TECH': 'Bio-Techne Corp.',
        'TEL': 'TE Connectivity Ltd.',
        'TER': 'Teradyne Inc.',
        'TFC': 'Truist Financial Corp.',
        'TFX': 'Teleflex Inc.',
        'TGT': 'Target Corp.',
        'TJX': 'TJX Cos. Inc.',
        'TMO': 'Thermo Fisher Scientific Inc.',
        'TMUS': 'T-Mobile US Inc.',
        'TPG': 'TPG Inc.',
        'TPR': 'Tapestry Inc.',
        'TRMB': 'Trimble Inc.',
        'TROW': 'T. Rowe Price Group Inc.',
        'TRV': 'Travelers Cos. Inc.',
        'TSCO': 'Tractor Supply Co.',
        'TSLA': 'Tesla Inc.',
        'TSN': 'Tyson Foods Inc.',
        'TT': 'Trane Technologies PLC',
        'TTWO': 'Take-Two Interactive Software Inc.',
        'TXN': 'Texas Instruments Inc.',
        'TXT': 'Textron Inc.',
        'TYL': 'Tyler Technologies Inc.',
        
        # U-V
        'UAL': 'United Airlines Holdings Inc.',
        'UDR': 'UDR Inc.',
        'UHS': 'Universal Health Services Inc.',
        'ULTA': 'Ulta Beauty Inc.',
        'UNH': 'UnitedHealth Group Inc.',
        'UNP': 'Union Pacific Corp.',
        'UPS': 'United Parcel Service Inc.',
        'URI': 'United Rentals Inc.',
        'USB': 'U.S. Bancorp',
        'V': 'Visa Inc.',
        'VFC': 'V.F. Corp.',
        'VLO': 'Valero Energy Corp.',
        'VMC': 'Vulcan Materials Co.',
        'VNO': 'Vornado Realty Trust',
        'VRSK': 'Verisk Analytics Inc.',
        'VRSN': 'VeriSign Inc.',
        'VRTX': 'Vertex Pharmaceuticals Inc.',
        'VTR': 'Ventas Inc.',
        'VTRS': 'Viatris Inc.',
        'VZ': 'Verizon Communications Inc.',
        
        # W-Z
        'WAB': 'Westinghouse Air Brake Technologies Corp.',
        'WAT': 'Waters Corp.',
        'WBA': 'Walgreens Boots Alliance Inc.',
        'WBD': 'Warner Bros. Discovery Inc.',
        'WDC': 'Western Digital Corp.',
        'WEC': 'WEC Energy Group Inc.',
        'WELL': 'Welltower Inc.',
        'WFC': 'Wells Fargo & Co.',
        'WHR': 'Whirlpool Corp.',
        'WM': 'Waste Management Inc.',
        'WMB': 'Williams Cos. Inc.',
        'WMT': 'Walmart Inc.',
        'WRB': 'W.R. Berkley Corp.',
        'WRK': 'WestRock Co.',
        'WST': 'West Pharmaceutical Services Inc.',
        'WTW': 'Willis Towers Watson PLC',
        'WY': 'Weyerhaeuser Co.',
        'XRAY': 'DENTSPLY SIRONA Inc.',
        'XYL': 'Xylem Inc.',
        'YUM': 'Yum! Brands Inc.',
        'ZBH': 'Zimmer Biomet Holdings Inc.',
        'ZBRA': 'Zebra Technologies Corp.',
        'ZION': 'Zions Bancorp NA',
        'ZTS': 'Zoetis Inc.'
    }


# ==========================================
# SECTOR MAPPINGS
# ==========================================
SECTOR_MAPPING = {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'CSCO', 'INTC', 'AMD', 'QCOM', 'TXN', 'AVGO', 'PYPL', 'UBER', 'SNOW'],
        'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'TFC', 'PNC', 'COF', 'AXP', 'BLK', 'SCHW', 'CB', 'ICE', 'CME', 'SPGI', 'MCO', 'V', 'MA'],
        'Healthcare': ['UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'ABT', 'LLY', 'MRK', 'BMY', 'AMGN', 'GILD', 'CVS', 'CI', 'ANTM', 'HUM', 'CNC', 'BIIB', 'REGN', 'VRTX', 'ISRG'],
        'Consumer Discretionary': ['HD', 'NKE', 'MCD', 'LOW', 'SBUX', 'TJX', 'BKNG', 'MAR', 'GM', 'F', 'CCL', 'RCL', 'MGM', 'DIS', 'CMCSA'],
        'Consumer Staples': ['WMT', 'PG', 'KO', 'PEP', 'COST', 'WBA', 'EL', 'CL', 'KMB', 'GIS', 'K', 'HSY', 'MDLZ'],
        'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'OXY', 'BKR'],
        'Industrials': ['BA', 'CAT', 'HON', 'UPS', 'RTX', 'LMT', 'GE', 'MMM', 'FDX', 'NOC', 'UNP', 'CSX', 'NSC'],
        'Materials': ['LIN', 'APD', 'ECL', 'FCX', 'NEM', 'DOW', 'DD', 'PPG', 'SHW', 'NUE'],
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'EXC', 'XEL', 'SRE', 'AEP', 'ES', 'AWK'],
        'Real Estate': ['AMT', 'CCI', 'PLD', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'WELL', 'SPG']
    }


# ==========================================
# QUICK CATEGORY MAPPINGS
# ==========================================
QUICK_CATEGORIES = {
                "🍎 Big Tech": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA'],
                "🏦 Major Banks": ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS'],
                "⚡ AI & Chips": ['NVDA', 'AMD', 'INTC', 'QCOM', 'AVGO'],
                "💊 Healthcare": ['UNH', 'JNJ', 'PFE', 'ABBV', 'MRK', 'LLY'],
                "🛒 Consumer": ['WMT', 'COST', 'HD', 'TGT', 'NKE', 'SBUX'],
                "⚡ Energy": ['XOM', 'CVX', 'COP', 'NEE', 'DUK'],
                "🏭 Industrial": ['BA', 'CAT', 'GE', 'HON', 'MMM', 'UPS'],
                "💰 Dividends": ['JNJ', 'PG', 'KO', 'PEP', 'MCD', 'WMT']
            }


# ==========================================
# UI CONSTANTS
# ==========================================

DEFAULT_SELECTED_SECTORS = ['Technology', 'Financial Services', 'Healthcare']
DEFAULT_STOCKS_PER_SECTOR = 8
ITEMS_PER_PAGE = 15
