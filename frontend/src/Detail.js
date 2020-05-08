import React, {useEffect, useState} from 'react'
import {b64toBlob} from "./utils";
import {withRouter, useLocation} from "react-router-dom";

export const Detail = () => {
    const [graySrc, setGraySrc] = useState("");
    const [imSrc, setImSrc] = useState("");
    const props = useLocation();
    useEffect(() => {
        console.log(props);
        const grayscale = window.sessionStorage.getItem("grayscale_b64");
        const im = window.sessionStorage.getItem("im_url");

        const blob_gray = b64toBlob(grayscale);
        const gray_url = URL.createObjectURL(blob_gray);
        setGraySrc(gray_url);
        setImSrc(im);
    }, [props]);
    return (
        <div style={more}>
            <img style={imgStyle} src={graySrc} alt={"Grayscale details"}/>
            <img style={imgStyle} src={imSrc} alt={"Detection result"}/>
        </div>
    )
};

const imgStyle = {
    display: 'block',
    maxWidth: '30vw',
    maxHeight: '24vh',
    width: 'auto',
    height: 'auto',
    margin: '0vh 5vw',
};

const more = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
};
