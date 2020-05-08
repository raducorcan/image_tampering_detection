export const DEFAULT_MSG = 'Drag file here, or click to browse file system';
export const baseStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    // padding: '2vh 0',
    margin: '5vh 5vw 5vh 5vw',
    minHeight: '50vh',
    borderWidth: 2,
    borderRadius: 2,
    borderColor: '#eeeeee',
    borderStyle: 'dashed',
    color: '#bdbdbd',
    outline: 'none',
    transition: 'border .24s ease-in-out'
};

export const activeStyle = {
    borderColor: '#2196f3'
};

export const acceptStyle = {
    borderColor: '#00e676',
    color: '#00e676'
};

export const rejectStyle = {
    borderColor: '#ff1744',
    color: '#ff1744'
};

export const thumbsContainer = {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 16
};

export const thumb = {
    display: 'inline-flex',
    marginLeft: '15vw',
    width: 200,
    height: 200,
    padding: 4,
    boxSizing: 'border-box'
};
//
export const thumbInner = {
    display: 'flex',
    minWidth: 0,
    overflow: 'hidden'
};

export const img = {
    display: 'block',
    width: 'auto',
    height: '100%'
};

export const errStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    // maxWidth: '50%',
    padding: '0 1vw',
    margin: '5vh 25vw 5vh 25vw',
    // minHeight: '30vh',
    borderWidth: 1.5,
    borderRadius: 5,
    borderColor: '#ff1744',
    borderStyle: 'solid',
    color: '#ff1744',
    backgroundColor: '#f0f0f0',
    outline: 'none'
};