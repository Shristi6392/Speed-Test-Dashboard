# import speedtest

# def run_speed_test():
#     st = speedtest.Speedtest()

#     print("Finding best server...")
#     st.get_best_server()

#     print("Testing download speed...")
#     download_speed = st.download() / 1_000_000  # Mbps

#     print("Testing upload speed...")
#     upload_speed = st.upload() / 1_000_000  # Mbps

#     ping = st.results.ping

#     return download_speed, upload_speed, ping


import speedtest

def run_speed_test():
    try:
        st = speedtest.Speedtest(secure=True)  # 🔥 important fix

        st.get_best_server()

        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping

        return download_speed, upload_speed, ping

    except Exception as e:
        return None, None, str(e)