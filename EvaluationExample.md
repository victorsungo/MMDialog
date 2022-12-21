## An Evaluation Example

#### Suppose we have a generated/retrieved multi-modal response:

$\tilde{R} = \lbrace \tilde{u}_1, \tilde{i}_1,\tilde{u}_2, \tilde{i}_2, \tilde{i}_3 \rbrace$

#### and the corresponding ground-truth response:

$R=\lbrace i_1,u_1, u_2, i_2, u_3 \rbrace$ 

#### where $u_j, i_j$ are the $j$-th textual and visual response element respectively.

#### We first align the textual (resp., visual) elements in predicted response and textual (resp., visual) elements in ground-truth response from the left:

$\tilde{R}_u = \lbrace \tilde{u}_1, \tilde{u}_2 \rbrace$ and $\tilde{R}_i = \lbrace \tilde{i}_1, \tilde{i}_2, \tilde{i}_3 \rbrace$

$R_u=\lbrace u_1, u_2, u_3 \rbrace$ and  $R_i= \lbrace i_1, i_2 \rbrace$ 

#### Then, evaluation metrics evaluated within a single modality (e.g., BLEU, Recall) can be obtained as follows.

#### For example, one can obtain the BLEU scores as:

$\text{BLEU-MM-Textual}(\tilde{R},R)= \frac{1}{3}(\text{BLEU}(\tilde{u}_1,u_1) + \text{BLEU}(\tilde{u}_2,u_2) + 0)$

#### Another example for computing the Recall scores for images is:

$\text{Recall-MM-Visual}(\tilde{R},R)= \frac{1}{2}(\text{Recall}(\tilde{i}_1,i_1) + \text{Recall}(\tilde{i}_2,i_2))$

### **Remark:**

#### When predicting $\tilde{i}_3$, as we do not have $i_3$ in ground-truth response $R$, the response retrieval model can only retrieve visual elements from the given negative elements in candidate set $C_v$.
