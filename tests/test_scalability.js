import http from "k6/http";
import { check, sleep } from "k6";

export function user() {
    const baseUrl = "http://your-api-url.com";
  
    // Step 1: Generate random username and password
    const account = JSON.stringify({
        "username": Math.random().toString(36),
        "password": Math.random().toString(36)
    });

    // Step 2: signup 
    const signupUrl = `${baseUrl}/signup`;
    const signupRes = http.post(signupUrl, account);

    check(signupRes, {
        "Signup successful": (res) => res.status === 200,
    });

    // Step 4: login
    const loginUrl = `${baseUrl}/login`;
    const loginRes = http.post(loginUrl, account);

    check(loginRes, {
        "Login successful": (res) => res.status === 200,
    });
    const authToken = JSON.parse(loginRes.body).token;
    const authHeader = { Authorization: `Bearer ${authToken}` };
    
    // Step 5: Program adds words for user to study 
    const dictionaryWord = "horse"; 
    const addWordPayload = JSON.stringify({ "word": dictionaryWord });
    const addWordUrl = `${baseUrl}/add_new_word`;
    const addWordRes = http.post(addWordUrl, addWordPayload, { headers: authHeader});

    check(addWordRes, {
        "Word added successfully": (res) => res.status === 200,
    });


    // Step 7: Get word to study
    const nextWordUrl = `${baseUrl}/next_word`;
    const nextWordRes = http.get(nextWordUrl, { headers: authHeader})
    
    check(nextWordRes, {
        "Next word retrieved successfully": (res) => res.status === 200,
    });

    const word = JSON.parse(nextWordRes.body).word;

    sleep(20); //user trying his best to remember word

    // Step 8: User clicks remember
    const studyPayLoad = JSON.stringify({
        "word": word,
        "result": "remember"
    }); 

    const updateWordUrl = `${baseUrl}/update_word`;
    const updateWordRes = http.put(updateWordUrl, studyPayLoad, { headers: authHeader});

    check(updateWordRes, {
        "Next word retrieved successfully": (res) => res.status === 200,
    });

    sleep(120); // User takes a break
}

export const options = { 
   scenarios: { 
      studier: { 
         exec: 'user', 
         executor: "ramping-vus", 
         stages: [ 
            { duration: "2m", target: 1000 }, 
            { duration: "2m", target: 2500 }, 
            { duration: "2m", target: 0 }, 
         ], 
      }, 
   }, 
};