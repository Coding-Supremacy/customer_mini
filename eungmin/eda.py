import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn import GraphConv

# Step 1: 데이터 로드 및 그래프 생성
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def create_graph(data):
    G = nx.Graph()
    
    # Add nodes with attributes
    for index, row in data.iterrows():
        G.add_node(row['이름'], age=row['연령'], gender=row['성별'], location=row['시구'])

    # Add edges based on the same location (시구)
    for i, row1 in data.iterrows():
        for j, row2 in data.iterrows():
            if i != j and row1['시구'] == row2['시구']:
                G.add_edge(row1['이름'], row2['이름'])
    
    return G

# Step 2: DGL 그래프로 변환
def nx_to_dgl(nx_graph):
    dgl_graph = dgl.from_networkx(nx_graph)
    return dgl_graph

# Step 3: GNN 모델 정의
class GCN(nn.Module):
    def __init__(self, in_feats, hidden_feats, out_feats):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, hidden_feats)
        self.conv2 = GraphConv(hidden_feats, out_feats)

    def forward(self, g, features):
        x = F.relu(self.conv1(g, features))
        x = self.conv2(g, x)
        return x

# Step 4: 데이터 준비 및 모델 학습
def prepare_and_train_model(graph):
    # 노드 피처(예: 연령)를 텐서로 변환
    node_features = torch.tensor([graph.nodes[n]['age'] for n in graph.nodes], dtype=torch.float32).unsqueeze(1)
    
    # DGL 그래프로 변환
    dgl_graph = nx_to_dgl(graph)
    
    # 모델 초기화
    model = GCN(in_feats=1, hidden_feats=16, out_feats=2)  # 입력 피처 크기=1 (연령), 출력 클래스=2 (예: 그룹화)
    
    # 옵티마이저 및 손실 함수 정의
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.CrossEntropyLoss()
    
    # 임의의 레이블 생성 (예제용)
    labels = torch.randint(0, 2, (len(graph.nodes),))  # 0 또는 1로 랜덤 레이블
    
    # 학습 루프
    for epoch in range(50):  # 에포크 수 조정 가능
        model.train()
        logits = model(dgl_graph, node_features)
        loss = loss_fn(logits, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
    
    return model

# Step 5: 결과 시각화 및 해석
def visualize_graph(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=8)
    plt.title("Customer Relationship Graph")
    st.pyplot(plt.gcf())

# 스트림릿 앱 실행 코드
def main():
    st.title("고객 데이터 기반 그래프 생성 및 분석")
    
    # 데이터 파일 업로드
    uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])
    
    if uploaded_file is not None:
        # 데이터 로드 및 미리보기
        data = load_data(uploaded_file)
        st.write("데이터 미리보기:")
        st.dataframe(data.head())
        
        # 그래프 생성 및 시각화
        customer_graph = create_graph(data)
        st.write("고객 관계 그래프:")
        visualize_graph(customer_graph)

        # 모델 학습 및 결과 출력
        st.write("모델 학습 중...")
        trained_model = prepare_and_train_model(customer_graph)
        st.write("모델 학습 완료!")

if __name__ == "__main__":
    main()
