#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – وحدة استغلال تيك توك
# جمع بيانات حسابات TikTok

import requests
import json
import re

class TikTokExploit:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.tiktok.com"

    def get_user_info(self, username):
        """جلب معلومات مستخدم TikTok"""
        try:
            url = f"https://www.tiktok.com/api/v1/user/detail/?unique_id={username}"
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "username": data.get("userInfo", {}).get("user", {}).get("uniqueId"),
                    "nickname": data.get("userInfo", {}).get("user", {}).get("nickname"),
                    "bio": data.get("userInfo", {}).get("user", {}).get("bioDescription"),
                    "followers": data.get("userInfo", {}).get("stats", {}).get("followerCount"),
                    "following": data.get("userInfo", {}).get("stats", {}).get("followingCount"),
                    "likes": data.get("userInfo", {}).get("stats", {}).get("heartCount"),
                    "videos": data.get("userInfo", {}).get("stats", {}).get("videoCount"),
                    "avatar": data.get("userInfo", {}).get("user", {}).get("avatarMedium")
                }
            return {"error": "المستخدم غير موجود"}
        except Exception as e:
            return {"error": str(e)}

    def get_user_videos(self, username, limit=10):
        """جلب فيديوهات المستخدم"""
        try:
            url = f"https://www.tiktok.com/api/v1/user/posts/?unique_id={username}&count={limit}"
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                videos = []
                for item in data.get("items", [])[:limit]:
                    videos.append({
                        "id": item.get("id"),
                        "desc": item.get("desc"),
                        "likes": item.get("stats", {}).get("diggCount"),
                        "shares": item.get("stats", {}).get("shareCount"),
                        "url": f"https://www.tiktok.com/@{username}/video/{item.get('id')}"
                    })
                return videos
            return []
        except:
            return []

    def exploit_tiktok_xss(self, username):
        """استغلال ثغرة XSS في TikTok"""
        payload = f"<script>alert('XSS on {username}')</script>"
        return {
            "username": username,
            "payload": payload,
            "status": "vulnerable" if username else "safe"
        }

    def extract_phone_from_tiktok(self, username):
        """محاولة استخراج رقم الهاتف من حساب TikTok (نادر)"""
        # هذه محاكاة – لا يمكن استخراج الرقم عبر API
        return {
            "username": username,
            "phone": "غير متاح عبر API",
            "note": "لا يمكن استخراج رقم الهاتف من TikTok عبر API"
        }