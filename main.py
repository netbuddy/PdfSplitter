import streamlit as st
import os
from PyPDF2 import PdfReader, PdfWriter
import tempfile

def split_pdf(input_path, output_path, page_ranges):
    pdf_reader = PdfReader(input_path)
    pdf_writer = PdfWriter()
    
    for start, end in page_ranges:
        for page in range(start - 1, min(end, len(pdf_reader.pages))):
            pdf_writer.add_page(pdf_reader.pages[page])
    
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

st.title("PDF文件切分工具")

def main():
    if 'splits' not in st.session_state:
        st.session_state.splits = []
    if 'total_pages' not in st.session_state:
        st.session_state.total_pages = 0

    # 1. 选择本地待切分的文件
    uploaded_file = st.file_uploader("选择PDF文件", type="pdf")

    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)

def process_uploaded_file(uploaded_file):
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # 读取临时PDF文件
    pdf_reader = PdfReader(uploaded_file)
    st.session_state.total_pages = len(pdf_reader.pages)
    st.write(f"文件总页数: {st.session_state.total_pages}")

    # 2. 设置切片的页码范围
    st.write("添加新切片")
    col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
    with col1:
        start_page = st.number_input("起始页码", min_value=1, max_value=st.session_state.total_pages, value=1, key="start_page")
    with col2:
        end_page = st.number_input("终止页码", min_value=start_page, max_value=st.session_state.total_pages, value=st.session_state.total_pages, key="end_page")
    with col3:
        default_filename = f"{os.path.splitext(uploaded_file.name)[0]}_{len(st.session_state.splits)+1}.pdf"
        new_filename = st.text_input("文件名", value=default_filename, key="new_filename")
    with col4:
        if st.button("添加切片"):
            st.session_state.splits.append(((start_page, end_page), new_filename))
            st.success(f"已添加切片: {start_page} - {end_page}")

    # 显示可编辑的切片列表
    if st.session_state.splits:
        st.write("切片列表:")
        for i, ((start, end), filename) in enumerate(st.session_state.splits):
            col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 1, 1])
            with col1:
                new_start = st.number_input(f"起始页码 {i+1}", min_value=1, max_value=st.session_state.total_pages, value=start, key=f"start_{i}")
            with col2:
                new_end = st.number_input(f"终止页码 {i+1}", min_value=new_start, max_value=st.session_state.total_pages, value=end, key=f"end_{i}")
            with col3:
                new_filename = st.text_input(f"文件名 {i+1}", value=filename, key=f"filename_{i}")
            with col4:
                if st.button("更新", key=f"update_{i}"):
                    st.session_state.splits[i] = ((new_start, new_end), new_filename)
                    st.success(f"切片 {i+1} 已更新")
            with col5:
                if st.button("删除", key=f"delete_{i}"):
                    st.session_state.splits.pop(i)
                    st.success(f"切片 {i+1} 已删除")
                    st.rerun()

    # 3. 选择保存路径
    save_path = st.text_input("保存路径", value=os.getcwd())

    # 4. 开始切分
    if st.button("开始切分"):
        for i, ((start, end), filename) in enumerate(st.session_state.splits, 1):
            output_filename = os.path.join(save_path, filename)
            with st.spinner(f"正在处理切片 {i}..."):
                split_pdf(tmp_file_path, output_filename, [(start, end)])
            st.success(f"切片 {i} 已保存为: {output_filename}")

        st.success("所有切片处理完成！")
    
    # 删除临时文件
    os.unlink(tmp_file_path)

if __name__ == "__main__":
    main()