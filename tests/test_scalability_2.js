import http from "k6/http";
import {check, sleep} from "k6";

export function studier() {
    const user_url = "http://dont-remember-123619125.us-east-1.elb.amazonaws.com/api/v1/users";
    const word_url = "http://dont-remember-123619125.us-east-1.elb.amazonaws.com/api/v1/words";

    // Step 1: Generate random username and password
    const account = JSON.stringify({
        username: Math.random().toString(36).slice(2),
        password: Math.random().toString(36).slice(2)
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Step 2: signup
    const signupUrl = `${user_url}/signup`;
    let signupRes = http.post(signupUrl, account, params);

    check(signupRes, {
        "Signup successful": (res) => res.status === 200,
    });

    // Step 4: login
    const loginUrl = `${user_url}/login`;
    const loginRes = http.post(loginUrl, account, params);

    check(loginRes, {
        "Login successful": (res) => res.status === 200,
    });
    const authToken = JSON.parse(loginRes.body).token;
    const authHeader = {
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        },
    };

    // Step 5: Program adds words for user to study
    const dictionaryWord = "horse";
    const addWordPayload = JSON.stringify({"word": dictionaryWord});
    const addWordUrl = `${word_url}/add_new_word`;
    const addWordRes = http.post(addWordUrl, addWordPayload, authHeader);

    check(addWordRes, {
        "Word added successfully": (res) => res.status === 200,
    });


    // Step 7: Get word to study
    const nextWordUrl = `${word_url}/next_word`;
    const nextWordRes = http.get(nextWordUrl, authHeader)

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

    const updateWordUrl = `${word_url}/update_word`;
    const updateWordRes = http.put(updateWordUrl, studyPayLoad, authHeader);

    check(updateWordRes, {
        "Next word retrieved successfully": (res) => res.status === 200,
    });

    sleep(20); // User takes a break
}

export const options = {
    scenarios: {
        studier: {
            exec: 'studier',
            executor: "ramping-vus",
            stages: [
                {duration: "4m", target: 200},
                {duration: "6m", target: 400},
                {duration: "6m", target: 667},
                {duration: "6m", target: 400},
                {duration: "4m", target: 200},
                {duration: "2m", target: 50}
            ],
        },
    }
};