#!/usr/bin/env python3
# 🔱 LØGHØST-Z 💀 – Crypto Cracker Module
# فك جميع أنواع تشفير بايثون المشفرة

import os
import re
import base64
import zlib
import marshal
import dis
import ast
import sys
import json
import hashlib
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from cryptography.fernet import Fernet
import pyarmor
import uncompyle6
import pyinstxtractor

# ============================================
# 1. فك تشفير Base64 (طبقات متعددة)
# ============================================
def decrypt_base64(data, layers=1):
    """فك تشفير Base64 بعدة طبقات"""
    try:
        result = data
        for _ in range(layers):
            result = base64.b64decode(result).decode('utf-8', errors='ignore')
        return result, None
    except Exception as e:
        return None, f"Base64 فشل: {str(e)}"

# ============================================
# 2. فك تشفير XOR
# ============================================
def decrypt_xor(data, key):
    """فك تشفير XOR مع مفتاح"""
    try:
        result = ''.join(chr(ord(c) ^ key) for c in data)
        return result, None
    except Exception as e:
        return None, f"XOR فشل: {str(e)}"

def auto_xor_crack(data):
    """كسر XOR تلقائياً بتجربة المفاتيح"""
    for key in range(1, 256):
        try:
            result = decrypt_xor(data, key)[0]
            if 'print' in result or 'def' in result or 'import' in result:
                return result, key
        except:
            continue
    return None, None

# ============================================
# 3. فك تشفير PyArmor
# ============================================
def decrypt_pyarmor(file_path):
    """فك تشفير ملفات PyArmor"""
    try:
        import subprocess
        output = subprocess.check_output(
            ['pyarmor', 'obfuscate', '--restore', file_path],
            stderr=subprocess.STDOUT,
            text=True
        )
        return output, None
    except Exception as e:
        return None, f"PyArmor فشل: {str(e)}"

# ============================================
# 4. فك تشفير AES
# ============================================
def decrypt_aes(encrypted_data, key, mode='ECB'):
    """فك تشفير AES"""
    try:
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 32:
            key_bytes = key_bytes.ljust(32, b'\0')
        elif len(key_bytes) > 32:
            key_bytes = key_bytes[:32]
        
        if mode == 'ECB':
            cipher = AES.new(key_bytes, AES.MODE_ECB)
            decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        elif mode == 'CBC':
            iv = encrypted_data[:16]
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
        else:
            return None, "وضع غير مدعوم"
        return decrypted.decode('utf-8', errors='ignore'), None
    except Exception as e:
        return None, f"AES فشل: {str(e)}"

# ============================================
# 5. فك تشفير Fernet
# ============================================
def decrypt_fernet(encrypted_data, key):
    """فك تشفير Fernet"""
    try:
        cipher = Fernet(key.encode())
        decrypted = cipher.decrypt(encrypted_data.encode())
        return decrypted.decode('utf-8'), None
    except Exception as e:
        return None, f"Fernet فشل: {str(e)}"

# ============================================
# 6. فك تشفير Zlib (ضغط)
# ============================================
def decompress_zlib(data):
    """فك ضغط Zlib"""
    try:
        decompressed = zlib.decompress(data)
        return decompressed.decode('utf-8', errors='ignore'), None
    except Exception as e:
        return None, f"Zlib فشل: {str(e)}"

# ============================================
# 7. فك تشفير Marshal (كود مترجم)
# ============================================
def unmarshal_code(data):
    """فك كود Marshal"""
    try:
        code = marshal.loads(data)
        return code, None
    except Exception as e:
        return None, f"Marshal فشل: {str(e)}"

# ============================================
# 8. فك ملفات PYInstaller
# ============================================
def extract_pyinstaller(file_path):
    """استخراج ملفات PYInstaller"""
    try:
        import pyi_archive
        import tempfile
        extract_dir = tempfile.mkdtemp()
        pyi_archive.extract(file_path, extract_dir)
        return extract_dir, None
    except Exception as e:
        return None, f"PYInstaller فشل: {str(e)}"

# ============================================
# 9. فك التشفير التلقائي (الذكي)
# ============================================
def auto_decrypt(content):
    """
    كشف نوع التشفير تلقائياً وفكه
    """
    results = []
    
    # 1. تحقق من Base64
    try:
        dec, err = decrypt_base64(content, 1)
        if dec and ('print' in dec or 'def' in dec or 'import' in dec):
            results.append(('Base64 (طبقة واحدة)', dec))
    except:
        pass
    
    # 2. تحقق من Base64 متعدد الطبقات
    for layers in range(2, 6):
        try:
            dec, err = decrypt_base64(content, layers)
            if dec and ('print' in dec or 'def' in dec or 'import' in dec):
                results.append((f'Base64 ({layers} طبقات)', dec))
                break
        except:
            pass
    
    # 3. تحقق من XOR
    try:
        dec, key = auto_xor_crack(content)
        if dec:
            results.append((f'XOR (مفتاح: {key})', dec))
    except:
        pass
    
    # 4. تحقق من Zlib
    try:
        import base64
        dec, err = decompress_zlib(base64.b64decode(content))
        if dec:
            results.append(('Zlib', dec))
    except:
        pass
    
    # 5. تحقق من Fernet
    try:
        # محاولة استخدام مفتاح افتراضي
        dec, err = decrypt_fernet(content, 'your-secret-key-here')
        if dec:
            results.append(('Fernet', dec))
    except:
        pass
    
    return results

# ============================================
# 10. واجهة البوت
# ============================================
async def decrypt_file_command(update, context):
    """أمر فك التشفير من البوت"""
    user = update.effective_user
    await update.message.reply_text(
        "🔓 **أداة فك التشفير المتقدمة**\n\n"
        "أرسل ملف `.py` المشفر، أو الصق النص المشفر مباشرة.\n"
        "سأقوم بكشف نوع التشفير تلقائياً وفكه.",
        parse_mode="Markdown"
    )
    context.user_data['mode'] = 'decrypt_file'

async def handle_decrypt_file(update, context):
    """معالجة ملف مشفر"""
    doc = update.message.document
    if doc and doc.file_name.endswith('.py'):
        file = await doc.get_file()
        temp_path = tempfile.mktemp()
        await file.download_to_drive(temp_path)
        with open(temp_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        results = auto_decrypt(content)
        
        if results:
            for method, decrypted in results:
                out_path = temp_path.replace('.py', f'_decrypted_{method.replace(" ", "_")}.py')
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(decrypted)
                await context.bot.send_document(
                    chat_id=user.id,
                    document=open(out_path, 'rb'),
                    caption=f"✅ تم الفك بـ {method}"
                )
                os.remove(out_path)
        else:
            await update.message.reply_text("❌ لم أتمكن من فك التشفير.")
        
        os.remove(temp_path)
        return

    # معالجة النص المشفر
    text = update.message.text
    results = auto_decrypt(text)
    if results:
        for method, decrypted in results:
            await update.message.reply_text(
                f"✅ **فك التشفير بـ {method}**\n\n```python\n{decrypted[:1500]}\n```",
                parse_mode="Markdown"
            )
    else:
        await update.message.reply_text("❌ لم أتمكن من فك التشفير.")

# ============================================
# 11. أوامر إضافية
# ============================================
async def decrypt_base64_cmd(update, context):
    """فك Base64"""
    await update.message.reply_text("📤 أرسل النص المشفر بـ Base64:")
    context.user_data['mode'] = 'base64'

async def decrypt_xor_cmd(update, context):
    """فك XOR"""
    await update.message.reply_text("📤 أرسل النص المشفر بـ XOR:")
    context.user_data['mode'] = 'xor'

async def decrypt_aes_cmd(update, context):
    """فك AES"""
    await update.message.reply_text(
        "📤 أرسل النص المشفر بـ AES مع المفتاح:\n"
        "مثال: `ciphertext|key|mode` (mode: ECB, CBC)",
        parse_mode="Markdown"
    )
    context.user_data['mode'] = 'aes'

async def handle_decrypt_text(update, context):
    """معالجة طلب فك التشفير"""
    user = update.effective_user
    text = update.message.text
    mode = context.user_data.get('mode')

    if mode == 'base64':
        dec, err = decrypt_base64(text, 3)
        if dec:
            await update.message.reply_text(f"✅ النص المفكك:\n\n```\n{dec[:1000]}\n```", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ {err}")
    
    elif mode == 'xor':
        dec, key = auto_xor_crack(text)
        if dec:
            await update.message.reply_text(f"✅ النص المفكك (مفتاح: {key}):\n\n```\n{dec[:1000]}\n```", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ لم أتمكن من كسر XOR.")
    
    elif mode == 'aes':
        parts = text.split('|')
        if len(parts) >= 2:
            encrypted = parts[0]
            key = parts[1]
            mode_aes = parts[2] if len(parts) > 2 else 'ECB'
            dec, err = decrypt_aes(encrypted.encode(), key, mode_aes)
            if dec:
                await update.message.reply_text(f"✅ النص المفكك:\n\n```\n{dec[:1000]}\n```", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"❌ {err}")
        else:
            await update.message.reply_text("❌ الصيغة غير صحيحة. استخدم: `ciphertext|key|mode`")

    context.user_data['mode'] = None