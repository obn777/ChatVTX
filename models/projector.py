import torch
import torch.nn as nn

class VisualProjector(nn.Module):
    def __init__(self, visual_dim: int, llm_dim: int, mlp_depth: int = 2):
        super().__init__()
        
        # Если глубина 1 — это простая линейная проекция
        if mlp_depth == 1:
            self.model = nn.Linear(visual_dim, llm_dim)
        else:
            # MLP с активацией GELU
            layers = [nn.Linear(visual_dim, llm_dim)]
            for _ in range(mlp_depth - 1):
                layers.append(nn.GELU())
                layers.append(nn.Linear(llm_dim, llm_dim))
            self.model = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: [batch_size, num_patches, visual_dim]
        return: [batch_size, num_patches, llm_dim]
        """
        return self.model(x)
