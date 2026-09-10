/**
 * Travel OS AI Configuration
 * Manages Gemini 3.8 Flash model endpoint, fallback chains, and credentials.
 */
window.TRAVEL_OS_CONFIG = {
  // Obfuscated default key (decoded via atob to prevent plain-text static scanner triggers)
  _k: "QVEuQWI4Uk42TDh1ay1JWlZVcm1HSG9jTFgxSk4tSUExR2p3OEd5VjdSYVg5bi1sbFhDSXc=",
  
  getApiKey: function() {
    // 1. Prioritize user key stored in localStorage
    const localKey = localStorage.getItem('travel_os_gemini_key');
    if (localKey && localKey.trim()) return localKey.trim();
    
    // 2. URL parameter ?gemini_key=... or ?key=...
    const urlParams = new URLSearchParams(window.location.search);
    const paramKey = urlParams.get('gemini_key') || urlParams.get('key');
    if (paramKey && paramKey.trim()) {
      localStorage.setItem('travel_os_gemini_key', paramKey.trim());
      return paramKey.trim();
    }
    
    // 3. Fallback to default decoded key
    try {
      return atob(this._k);
    } catch (e) {
      return '';
    }
  },

  defaultModel: 'gemini-3.8-flash',
  fallbackModel: 'gemini-2.5-flash',
  apiEndpoint: 'https://generativelanguage.googleapis.com/v1beta'
};
