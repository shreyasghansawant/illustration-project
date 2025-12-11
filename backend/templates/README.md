# Template Images

Place your template illustration images here.

## Template Requirements

- Format: PNG (with transparency support recommended)
- Recommended size: 1024x1024 or larger
- Face area: Should be in the center or marked area

## Adding a Template

1. Place your template image in this directory
2. Name it `template.png` for the default template
3. Or use custom names and specify in the API call

## Template Design Tips

- Leave space in the center for the face
- Use transparent backgrounds for better blending
- Ensure good contrast between face area and background
- Consider the aspect ratio of typical photos (portrait orientation works well)

## Example Template Structure

```
template.png          # Default template
template_cartoon.png  # Cartoon style template
template_book.png     # Children's book style template
```

The system will automatically composite the personalized face into the template.

