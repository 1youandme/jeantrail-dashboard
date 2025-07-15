def check_railway_usage():
    headers = {
        "Authorization": f"Bearer {RAILWAY_TOKEN}",
        "Content-Type": "application/json"
    }

    query = {
        "query": """
            {
                me {
                    usage {
                        usageAmount
                        usageLimit
                    }
                }
            }
        """
    }

    try:
        res = requests.post("https://backboard.railway.app/graphql", headers=headers, json=query)
        if res.status_code == 200:
            usage_data = res.json()
            usage = usage_data["data"]["me"]["usage"]["usageAmount"]
            limit = usage_data["data"]["me"]["usage"]["usageLimit"]

            if usage >= limit * 0.8:
                msg = f"🚨 Railway usage high: {usage:.2f}$ of {limit:.2f}$ used."
                send_email("تنبيه استهلاك Railway", msg)
                send_telegram(msg)
            else:
                print(f"✅ Railway usage is fine: {usage:.2f}$ of {limit:.2f}$")
        else:
            print("❌ Failed to fetch Railway usage.")
            print("Status code:", res.status_code)
            print("Response body:", res.text)
    except Exception as e:
        print(f"❌ Error: {e}")
