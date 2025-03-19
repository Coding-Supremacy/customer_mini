import streamlit as st

# 이미지 URL 리스트 (또는 로컬 이미지 경로 사용 가능)
image_urls = [
    "D:\junghee\GitHub\customer_mini\img\home.png", 
    "img/hyundai_logo.jpg", 
    "img/welcome.png"
]

# 캐러셀 HTML 및 JS 코드
carousel_html = f"""
<style>
    .carousel-container {{
        position: relative;
        width: 100%;
        max-width: 900px;
        margin: auto;
        text-align: center;
    }}
    
    .carousel-image {{
        width: 100%;
        border-radius: 10px;
        transition: opacity 0.5s ease-in-out;
    }}

    /* 화살표 스타일 */
    .carousel-arrow {{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        font-size: 30px;
        padding: 10px;
        cursor: pointer;
        border-radius: 50%;
    }}
    
    .prev {{
        left: 10px;
    }}
    
    .next {{
        right: 10px;
    }}

    /* 하단 페이지 인디케이터 스타일 */
    .dot-container {{
        text-align: center;
        margin-top: 10px;
    }}
    
    .dot {{
        height: 12px;
        width: 12px;
        margin: 5px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: background-color 0.3s;
    }}

    .active {{
        background-color: #005bac;
    }}
</style>

<div class="carousel-container">
    <button class="carousel-arrow prev" onclick="prevImage()">&#10094;</button>
    <img id="carousel-image" src="{image_urls[0]}" class="carousel-image">
    <button class="carousel-arrow next" onclick="nextImage()">&#10095;</button>

    <!-- 페이지 인디케이터 -->
    <div class="dot-container">
        {''.join(f'<span class="dot" onclick="goToImage({i})"></span>' for i in range(len(image_urls)))}
    </div>
</div>

<script>
    var images = {image_urls};
    var index = 0;
    
    function updateCarousel() {{
        document.getElementById("carousel-image").src = images[index];
        updateDots();
    }}
    
    function prevImage() {{
        index = (index - 1 + images.length) % images.length;
        updateCarousel();
    }}
    
    function nextImage() {{
        index = (index + 1) % images.length;
        updateCarousel();
    }}

    function goToImage(n) {{
        index = n;
        updateCarousel();
    }}

    function updateDots() {{
        var dots = document.getElementsByClassName("dot");
        for (var i = 0; i < dots.length; i++) {{
            dots[i].classList.remove("active");
        }}
        dots[index].classList.add("active");
    }}

    updateDots();  // 초기 상태 업데이트
</script>
"""

# 스트림릿에서 HTML 코드 실행
st.components.v1.html(carousel_html, height=500)
