"""
آپلودرهای ایرانی - Iranian Uploaders Module
"""
import os
import re
import requests
from urllib.parse import urlparse, unquote
import logging

logger = logging.getLogger(__name__)


class UplodIrUploader:
    """
    آپلودر uplod.ir
    """
    BASE_URL = "https://uplod.ir"
    
    def __init__(self, token=None):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def upload_file(self, file_path, on_progress=None):
        """
        آپلود فایل به uplod.ir
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"فایل یافت نشد: {file_path}")
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        logger.info(f"شروع آپلود فایل: {file_name} ({file_size} بایت)")
        
        # Step 1: Get upload server
        try:
            server_resp = self.session.get(
                f"{self.BASE_URL}/upload.php",
                params={"JsSize": file_size}
            )
            
            # Extract upload server URL from response
            server_match = re.search(r'upload_server_url.*?"(https?://[^"]+)"', server_resp.text)
            if not server_match:
                server_match = re.search(r'(https?://s[0-9]+\.uplod\.ir/[^"]+)', server_resp.text)
            
            if server_match:
                upload_url = server_match.group(1)
            else:
                upload_url = f"{self.BASE_URL}/upload.php"
        except Exception as e:
            logger.warning(f"خطا در دریافت سرور آپلود: {e}")
            upload_url = f"{self.BASE_URL}/upload.php"
        
        # Step 2: Upload file
        with open(file_path, "rb") as f:
            files = {
                "file": (file_name, f, "application/octet-stream")
            }
            
            data = {
                "file_name": file_name,
                "file_size": file_size,
            }
            
            if self.token:
                data["token"] = self.token
            
            try:
                resp = self.session.post(
                    upload_url,
                    files=files,
                    data=data,
                    timeout=300
                )
                
                if resp.status_code == 200:
                    # Parse response
                    result = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else None
                    
                    if result:
                        download_url = result.get("file_url") or result.get("url") or result.get("link")
                        if download_url:
                            return {"success": True, "url": download_url, "uploader": "uplod.ir"}
                    
                    # Try to extract URL from HTML response
                    url_match = re.search(r'(https?://(?:www\.)?uplod\.ir/[a-zA-Z0-9]+)', resp.text)
                    if url_match:
                        return {"success": True, "url": url_match.group(1), "uploader": "uplod.ir"}
                    
                    return {"success": False, "error": "پاسخ سرور نامعتبر", "uploader": "uplod.ir"}
                else:
                    return {"success": False, "error": f"خطای سرور: {resp.status_code}", "uploader": "uplod.ir"}
                    
            except Exception as e:
                return {"success": False, "error": str(e), "uploader": "uplod.ir"}


class LinkNimConverter:
    """
    تبدیل لینک به نیم بها با استفاده از linknim.ir
    """
    BASE_URL = "https://linknim.ir"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def prepare_link(self, url):
        """
        آماده‌سازی لینک برای دانلود نیم بها
        """
        try:
            resp = self.session.post(
                f"{self.BASE_URL}/dl/",
                data={"url": url, "step": "send link"},
                timeout=30
            )
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"خطا در آماده‌سازی لینک: {e}")
            return False
    
    def download_file(self, url, output_path):
        """
        دانلود فایل از طریق linknim.ir
        """
        try:
            with self.session.post(
                f"{self.BASE_URL}/dl/",
                data={"url": url, "res": "download"},
                stream=True,
                timeout=600
            ) as resp:
                resp.raise_for_status()
                
                with open(output_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return {"success": True, "path": output_path, "uploader": "linknim.ir"}
        except Exception as e:
            return {"success": False, "error": str(e), "uploader": "linknim.ir"}


class UploadKonUploader:
    """
    آپلودر uploadkon.ir
    """
    BASE_URL = "https://uploadkon.ir"
    
    def __init__(self, token=None):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def upload_file(self, file_path, on_progress=None):
        """
        آپلود فایل به uploadkon.ir
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"فایل یافت نشد: {file_path}")
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        logger.info(f"شروع آپلود فایل: {file_name} ({file_size} بایت)")
        
        try:
            with open(file_path, "rb") as f:
                files = {
                    "file": (file_name, f, "application/octet-stream")
                }
                
                resp = self.session.post(
                    f"{self.BASE_URL}/upload.php",
                    files=files,
                    timeout=300
                )
                
                if resp.status_code == 200:
                    # Try to extract URL from response
                    url_match = re.search(r'(https?://(?:www\.)?uploadkon\.ir/[a-zA-Z0-9]+)', resp.text)
                    if url_match:
                        return {"success": True, "url": url_match.group(1), "uploader": "uploadkon.ir"}
                    
                    # Try JSON response
                    try:
                        result = resp.json()
                        download_url = result.get("file_url") or result.get("url") or result.get("link")
                        if download_url:
                            return {"success": True, "url": download_url, "uploader": "uploadkon.ir"}
                    except:
                        pass
                    
                    return {"success": False, "error": "پاسخ سرور نامعتبر", "uploader": "uploadkon.ir"}
                else:
                    return {"success": False, "error": f"خطای سرور: {resp.status_code}", "uploader": "uploadkon.ir"}
                    
        except Exception as e:
            return {"success": False, "error": str(e), "uploader": "uploadkon.ir"}


class UploaderManager:
    """
    مدیریت آپلودرهای مختلف
    """
    
    def __init__(self):
        self.uploaders = {
            "uplod": UplodIrUploader(),
            "uploadkon": UploadKonUploader(),
        }
        self.link_converter = LinkNimConverter()
    
    def get_uploader(self, name):
        """
        دریافت آپلودر با نام
        """
        return self.uploaders.get(name)
    
    def list_uploaders(self):
        """
        لیست آپلودرهای موجود
        """
        return list(self.uploaders.keys())
    
    def upload_with_fallback(self, file_path, preferred_uploader=None):
        """
        آپلود فایل با fallback به آپلودرهای دیگر
        """
        uploaders_to_try = []
        
        if preferred_uploader and preferred_uploader in self.uploaders:
            uploaders_to_try.append(preferred_uploader)
            for name in self.uploaders:
                if name != preferred_uploader:
                    uploaders_to_try.append(name)
        else:
            uploaders_to_try = list(self.uploaders.keys())
        
        for name in uploaders_to_try:
            uploader = self.uploaders[name]
            try:
                result = uploader.upload_file(file_path)
                if result["success"]:
                    return result
                else:
                    logger.warning(f"آپلودر {name} ناموفق: {result.get('error')}")
            except Exception as e:
                logger.error(f"خطا در آپلودر {name}: {e}")
        
        return {"success": False, "error": "همه آپلودرها ناموفق بودند"}
