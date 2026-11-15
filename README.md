# bedava-video

Metinden **tamamen ücretsiz** video üreten küçük bir Python aracı. Hesap, API anahtarı veya ödeme gerekmez.

## Kurulum

```bash
pip install -r requirements.txt
```

(moviepy, ffmpeg'i otomatik getirir.)

## Kullanım

1. `scenes.json` içine sahnelerini yaz:
   ```json
   [{"text": "İlk sahne", "seconds": 4}, {"text": "İkinci sahne"}]
   ```
2. Çalıştır:
   ```bash
   python make_video.py            # sessiz
   python make_video.py --voice    # Türkçe sesli anlatım (internet gerekir)
   ```
3. Çıktı: `video.mp4`

## Seçenekler

| Seçenek | Açıklama |
|---|---|
| `--scenes` | Sahne dosyası (varsayılan `scenes.json`) |
| `--out` | Çıktı dosyası (varsayılan `video.mp4`) |
| `--voice` | edge-tts ile seslendirme |
| `--voice-name` | Ses (örn. `tr-TR-EmelNeural`) |
| `--default-seconds` | Sessiz modda sahne süresi |

## Ücretsiz Kaynaklar

- Görüntü: Pillow ile çizim (istersen kendi görsellerini ekleyebilirsin)
- Ses: edge-tts
- Birleştirme: moviepy + ffmpeg

## Lisans
MIT
