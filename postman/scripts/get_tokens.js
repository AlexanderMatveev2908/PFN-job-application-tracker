const data = pm.response.json();
if (data?.access_token) {
  pm.environment.set("access_token", data.access_token);
}
if (data?.cbc_hmac_token) {
  pm.environment.set("cbc_hmac_token", data.cbc_hmac_token);
}
