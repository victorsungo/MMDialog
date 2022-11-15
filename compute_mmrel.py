from PIL import Image
from transformers import CLIPProcessor, CLIPTokenizer, CLIPModel
import torch


model_type="openai/clip-vit-base-patch32"
processor = CLIPProcessor.from_pretrained(model_type)
clip_tokenizer = CLIPTokenizer.from_pretrained(model_type)
clip_model = CLIPModel.from_pretrained(model_type)
vision_model = clip_model.vision_model
text_model = clip_model.text_model


def get_visual_embeds(session_imgs):
    # process visual elements
    session_img_pil = [Image.open(img) for img in session_imgs]
    session_vision_inputs = processor(images=session_img_pil, return_tensors='pt')
    session_vision_outputs = vision_model(**session_vision_inputs)
    session_vision_embeds = session_vision_outputs[1]
    session_vision_embeds = clip_model.visual_projection(session_vision_embeds)
    session_vision_embeds = session_vision_embeds / session_vision_embeds.norm(p=2, dim=-1, keepdim=True)
    
    return session_vision_embeds

def get_text_embeds(session_utts):
    # process textual elements
    session_text_inputs = processor.tokenizer(session_utts, padding=True, truncation=True, return_tensors="pt")
    session_text_outputs = text_model(**session_text_inputs)
    session_text_embeds = session_text_outputs[1]
    session_text_embeds = clip_model.text_projection(session_text_embeds)
    session_text_embeds = session_text_embeds / session_text_embeds.norm(p=2, dim=-1, keepdim=True)
    
    return session_text_embeds

if __name__ == "__main__":
    # please refer to source codes of CLIP in HuggingFace
    logit_scale = clip_model.logit_scale.exp()
    
    # assume that we have a reference response: ref 
    # and a generated response: hyp
    demo_hyp = ['Hi', 'demo.jpg']
    demo_ref = ['demo.jpg', 'Hello World!']
    
    hyp_embs = [get_text_embeds(demo_hyp[0]).squeeze(), get_visual_embeds([demo_hyp[1]]).squeeze()]
    ref_embs = [get_visual_embeds([demo_ref[0]]).squeeze(), get_text_embeds(demo_ref[1]).squeeze()]

    for hyp_emb, ref_emb in zip(hyp_embs, ref_embs):
        clip_score = torch.matmul(hyp_emb.unsqueeze(0), ref_emb.unsqueeze(1)).squeeze() * logit_scale
        print(clip_score.item())