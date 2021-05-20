const REDIRECT_AUTH_URI = `${process.env.NODE_ENV === 'development' ? 'http://localhost:3000/login' : 'https://web.azerp.xyz/login'}`;
// export const DOMAIN = 'https://api.azerp.xyz';
export const DOMAIN = 'http://127.0.0.1:8001';

export const msalConfig = {
    auth: {
        clientId: "ec359746-8d5d-4aa9-8ed3-4f42b862c427",
        authority: "https://login.microsoftonline.com/common",
        redirectUri: REDIRECT_AUTH_URI,
        grant_type: 'code',
    },
    cache: {
        cacheLocation: "sessionStorage", // This configures where your cache will be stored
        storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
    },
};

export const loginRequest = {
    scopes: ["User.Read"]
};