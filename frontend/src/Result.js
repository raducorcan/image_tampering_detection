import React, {useEffect, useState} from "react";
import AnimateHeight from "react-animate-height";
import {MdCheckCircle, MdWarning} from "react-icons/md";
import {Link} from "react-router-dom";

const Result = ({imgSrc, percentage}) => {
    const [height, setHeight] = useState('auto'); //remove to keep result image
    useEffect(() => () => {
        setHeight(0);
    });

    return (
        <AnimateHeight
            duration={500}
            height={height}
        >
            <div className='area'>
                <img src={imgSrc} style={imgStyle} alt='Detection result'/>
                <div style={more}>
                    <div>
                        {percentage === "0.00" &&
                        <div style={{...percStyle, color: '#01cb00', borderColor: '#01cb00'}}>
                            <MdCheckCircle style={{marginRight: '1vw'}} size={36}/>
                            <p style={{color: '#01cb00', fontWeight: 'bold'}}>Image is untampered!</p>

                        </div>
                        }
                        {percentage !== "0.00" &&
                        <div style={{...percStyle, color: '#eadb00', borderColor: '#eadb00'}}>
                            <MdWarning style={{marginRight: '1vw'}} size={36}/>
                            <p style={{color: '#eadb00', fontWeight: 'bold'}}>Tampering detected!
                                Percentage: {percentage}</p>

                        </div>
                        }
                    </div>
                    <a id="link_btn" href={imgSrc} download={"im.png"}>SAVE IMAGE</a>
                    <Link id="link_btn" to={{
                        pathname: "/detail",
                        state: "42",
                    }} target={'_blank'}>DETAILED INFO</Link>
                </div>
            </div>
        </AnimateHeight>
    );
};

const imgStyle = {
    display: 'block',
    maxWidth: '30vw',
    maxHeight: '24vh',
    width: 'auto',
    height: 'auto',
    margin: '5vh 0 5vh 0',
};

const more = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '2vh 0 2vh 10vw',
    padding: 16,
};

const percStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '0 1vw',
    margin: '2vh 0vw',
    borderWidth: 1.5,
    borderRadius: 5,
    // borderColor: '#01cb00',
    borderStyle: 'solid',
    // color: '#01cb00',
    outline: 'none'
};

export default Result;