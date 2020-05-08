import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import { Link, Element , Events, animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'
import GridLoader from "react-spinners/GridLoader";
import {
    acceptStyle,
    activeStyle,
    baseStyle,
    DEFAULT_MSG,
    img,
    rejectStyle,
    thumb,
    thumbInner,
    thumbsContainer
} from './styles'
import ErrorBox from "./ErrorBox";
import Result from "./Result";
import {b64toBlob} from "./utils";

function StyledDropzone() {
    const [files, setFiles] = useState([]);
    const [isError, setIsError] = useState(false);
    const [resultUrl, setResultUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [percentage, setPercentage] = useState(null);

    const {
        getRootProps,
        getInputProps,
        isDragActive,
        isDragAccept,
        isDragReject
    } = useDropzone({
        accept: 'image/*',
        onDropAccepted: acceptedFiles => {
            setFiles(acceptedFiles.map(file => Object.assign(file, {
                preview: URL.createObjectURL(file)
            })));
        },
        onDropRejected: rejectedFiles => {
            setIsError(true);
            setTimeout(() => {
                setIsError(false);
            }, 5000);
        }
    });

    const style = useMemo(() => ({
        ...baseStyle,
        ...(isDragActive ? activeStyle : {}),
        ...(isDragAccept ? acceptStyle : {}),
        ...(isDragReject ? rejectStyle : {}),
    }), [isDragAccept, isDragActive, isDragReject]);

    const thumbs = useMemo(() => files.map(file => {
        console.log(file.size / (1024 * 1024) + 'MB');
        return (
            <div style={thumb} key={file.name}>
                <div style={thumbInner}>
                    <img
                        src={file.preview}
                        style={img}
                        alt={'Preview of uploaded file'}/>
                </div>
            </div>
        )
    }), [files]);

    // useEffect(() => () => {
    //     files.forEach(file => URL.revokeObjectURL(file.preview));
    // }, [files]);

    const submitImage = useCallback(async () => {
        let blob = await fetch(files[0].preview).then(r => r.blob());
        const data = new FormData();
        data.append('image', blob);
        setLoading(true);
        fetch('http://192.168.1.7:5000/detect', {
            method: 'POST',
            body: data
        }).then(resp => resp.json())
            .then((json) => {
                console.log(json.percentage);
                const recv_percentage = parseFloat(json.percentage);

                const blob_im = b64toBlob(json.im);
                const url_im = URL.createObjectURL(blob_im);

                setFiles([]);
                setResultUrl(url_im);
                setPercentage(recv_percentage);
                setLoading(false);

                window.sessionStorage.setItem("grayscale_b64", json.grayscale);
                window.sessionStorage.setItem("im_url", url_im);

                scroller.scrollTo('resultElem', {
                    duration: 1500,
                    smooth: true,
                    offset: 50,
                })
            });
    }, [files]);

    return (
        <div>
            <ErrorBox showing={isError}/>
            <section className="container">
                <div {...getRootProps({style})}>
                    <input {...getInputProps()} />
                    {isDragAccept && files.length > 0 && <p>File accepted (will replace existing image)</p>}
                    {isDragAccept && files.length === 0 && <p>File accepted</p>}
                    {isDragReject && <p>Bad filetype</p>}
                    {!isDragActive && <p>{DEFAULT_MSG}</p>}
                    {files && !isDragActive && <aside style={thumbsContainer}>
                        {thumbs}
                    </aside>}
                </div>
            </section>
            <div className='area'>
                {files.length > 0 && !loading && <button id='submit' onClick={submitImage}>
                    SUBMIT
                </button>}
            </div>
            <Element name='resultElem' className='area'>
                <GridLoader
                    size={50}
                    color={"wheat"}
                    loading={loading}
                />
                {resultUrl && !loading && <Result imgSrc={resultUrl} percentage={percentage.toFixed(2)}/>}
                {/*{resultUrlGray && !loading && <Result src={resultUrlGray}/>}*/}
            </Element>
        </div>
    );
}

export default StyledDropzone