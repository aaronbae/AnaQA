# AnaQA
Multi-Hop Question Answering system based on DecompRC and Dr.QA. The goal is to replace the single-hop question answering engien in DecompRC with DrQA system. The goal was to see if the the answer accuracy will further improve if it were to use a different single-hop answering engine. 

![AnaQA Results](https://github.com/aaronbae/AnaQA/blob/master/anaqa-results.PNG)
As apparent in the table above, the result was unfortunately poorer than the original DecompRC. However, significant insight related to question-answer model was observed. You can see the final report in this repo or from this link here: https://github.com/aaronbae/AnaQA/blob/master/NLP_Project_Report.pdf

## Important Notes to Run
Make sure that you have the "model" folder from DecompRC and "data" folder from DrQA. Also, you will need the Hoptpot QA dataset in an additional folder called "dataset". These data are not included becasue of the size issue. Here are links to download them:
- DecompRC: https://github.com/shmsw25/DecompRC
- DrQA: https://github.com/facebookresearch/DrQA
- HotpotQA: https://hotpotqa.github.io/

## Citation
We recognize that the project is largely an attempt to combine two different projects together. Here are the 2 projects that we reference:
1. DecompRC:
  - Git: https://github.com/shmsw25/DecompRC
  - Paper: https://arxiv.org/pdf/1906.02916.pdf
2. DrQA:
  - Git: https://github.com/facebookresearch/DrQA
  - Paper: https://arxiv.org/pdf/1704.00051.pdf
