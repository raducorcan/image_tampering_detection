import AnimateHeight from "react-animate-height";
import { MdErrorOutline } from "react-icons/md";
import React from "react";
import {errStyle} from "./styles";

const ErrorBox = ({showing}) => {
    return (
        <AnimateHeight
            duration={1000}
            height={showing ? 125 : 0}
        >
            <div style={errStyle}>
                <MdErrorOutline style={{marginRight: '1vw'}} size={48}/>
                <p>File not accepted! Supported types: jpg, png, tiff, or other image formats.</p>
            </div>
        </AnimateHeight>
    )
};

export default ErrorBox