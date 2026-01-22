// Automated Page Crawler for Proppy.com.au
// This script systematically visits all pages and extracts content

const pages = {
  main: [
    { name: '01-homepage', url: 'https://proppy.com.au/' },
    { name: '02-about-us', url: 'https://proppy.com.au/about-us' },
    { name: '03-contact-us', url: 'https://proppy.com.au/contact-us' },
    { name: '04-investor-assessment', url: 'https://proppy.com.au/investor-assessment-session' },
    { name: '05-faq', url: 'https://proppy.com.au/faq' },
    { name: '06-get-started', url: 'https://proppy.com.au/get-started' },
    { name: '07-how-we-do-it', url: 'https://proppy.com.au/how-we-do-it' },
    { name: '08-investor-guides', url: 'https://proppy.com.au/investor-guides' },
    { name: '09-investor-updates', url: 'https://proppy.com.au/investor-updates' },
    { name: '10-market-updates', url: 'https://proppy.com.au/market-updates' },
    { name: '11-money-back-guarantee', url: 'https://proppy.com.au/money-back-guarantee' },
    { name: '12-our-results', url: 'https://proppy.com.au/our-results' },
    { name: '13-our-technology', url: 'https://proppy.com.au/our-technology' },
    { name: '14-pricing', url: 'https://proppy.com.au/pricing' },
    { name: '15-privacy-policy', url: 'https://proppy.com.au/privacy-policy' },
    { name: '16-properties-we-source', url: 'https://proppy.com.au/properties-we-source' },
    { name: '17-reviews-testimonials', url: 'https://proppy.com.au/reviews-and-customer-testimonials' },
    { name: '18-terms-conditions', url: 'https://proppy.com.au/terms-and-conditions' },
    { name: '19-what-we-do', url: 'https://proppy.com.au/what-we-do' },
    { name: '20-why-choose-proppy', url: 'https://proppy.com.au/why-choose-proppy' },
    { name: '21-sitemap', url: 'https://proppy.com.au/sitemap' },
  ],

  investorGuides: [
    { name: 'purchase-through-trust', url: 'https://proppy.com.au/investor-guides/purchase-investment-property-through-trust' }
  ],

  marketUpdates: [
    { name: 'august-2025', url: 'https://proppy.com.au/market-updates/august-2025-market-update' },
    { name: 'july-2025', url: 'https://proppy.com.au/market-updates/july-2025-market-update' },
    { name: 'june-2025', url: 'https://proppy.com.au/market-updates/june-2025-market-update' },
    { name: 'may-2025', url: 'https://proppy.com.au/market-updates/may-2025-market-update' },
    { name: 'april-2025', url: 'https://proppy.com.au/market-updates/april-2025-market-update' },
    { name: 'march-2025', url: 'https://proppy.com.au/market-updates/march-2025-market-update' },
    { name: 'february-2025', url: 'https://proppy.com.au/market-updates/february-2025-market-update' },
    { name: 'january-2025', url: 'https://proppy.com.au/market-updates/january-2025-market-update' },
    { name: 'december-2024', url: 'https://proppy.com.au/market-updates/december-2024-marker-update' },
    { name: 'november-2024', url: 'https://proppy.com.au/market-updates/november-2024-market-update' },
    { name: 'october-2024', url: 'https://proppy.com.au/market-updates/october-2024-market-update' },
    { name: 'september-2024', url: 'https://proppy.com.au/market-updates/september-2024-market-update' },
  ],

  properties: [
    { name: 'hastings-coastal-gem', url: 'https://proppy.com.au/property/a-high-growth-high-yield-coastal-investment-gem' },
    { name: 'hastings-waterfront', url: 'https://proppy.com.au/property/waterfront-cottage-in-hastings-exceptional-capital-growth-income-potential' },
    { name: 'hastings-high-yield', url: 'https://proppy.com.au/property/incredible-investment-property-in-morning-peninsula' },
    { name: 'albion-exceptional', url: 'https://proppy.com.au/property/exceptional-capital-rental-growth-albions-26-mclean-street-is-a-savvy-investors-dream' },
    { name: 'reservoir-rare', url: 'https://proppy.com.au/property/reservoir-gem-with-solid-cashflow-and-high-capital-upside' },
    { name: 'reservoir-strong-rental', url: 'https://proppy.com.au/property/strong-rental-returns-steady-growth-an-ideal-entry-into-the-reservoir-investment-market' },
    { name: 'seaford-rare-block', url: 'https://proppy.com.au/property/rare-seaford-block-bought-dirt-cheap' },
    { name: 'thornbury-standout', url: 'https://proppy.com.au/property/high-growth-strong-yield-this-is-a-standout-investment-in-thornbury' },
    { name: 'richmond-gem', url: 'https://proppy.com.au/property/richmond-gem-exceptional-capital-rental-growth' },
  ]
};

// Full list for reference
const allPages = [
  ...pages.main,
  ...pages.investorGuides,
  ...pages.marketUpdates,
  ...pages.properties
];

console.log(`Total pages to crawl: ${allPages.length}`);
console.log(JSON.stringify(allPages, null, 2));
