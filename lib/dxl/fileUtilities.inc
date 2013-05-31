// Provide functions for reading and writing files without leaks 


// *************************** Each time a file is opened for read or write a Stream is leaked ***********************
// *************************** Therefore we use eval_ to write and read files ****************************************

Buffer *gBufWriteTextContentBuffer
Buffer gBufTextFilenameBuffer = create()
int gIntTextfileCodepage = CP_UTF8
bool gBoolAppendTextFile = false

string gStrWriteBufferCode = "
    // we use that double pointer to not have to copy the buffer contents
    Buffer **bufTextContentBufferDblPtr  = addr_ " ((addr_ (&gBufWriteTextContentBuffer)) int) "
    Buffer bufTextFilenameBuffer = (addr_ " ((addr_ gBufTextFilenameBuffer) int) ") Buffer
    int &iCodepage = addr_ " ((addr_ (&gIntTextfileCodepage)) int) "
    bool &bAppendRef  = addr_ " ((addr_ (&gBoolAppendTextFile)) int) "
    bool bAppend = bAppendRef
    
    Buffer &bufText = **bufTextContentBufferDblPtr
    string strErr = null

    // Create file and write contents; and catch errors if any
    Stream os = null
    
    noError
    if (bAppend == false) {
        os = write( bufTextFilenameBuffer \"\", iCodepage )
    } else { 
        os = append ( bufTextFilenameBuffer \"\", iCodepage )
    }
    
    if (!null (strErr = lastError())) { return_ strErr; halt }
    
    noError()
    
    // Write needed contents to the batch file stream:
    os << bufText
    
    // Save stream contents to file and close it
    close( os )
    
    return_ lastError()
"

string writeOrAppendFileWithoutLeak (string file_Name, Buffer fileContent, int codepage, bool bAppend) {
    gBufTextFilenameBuffer = file_Name
    gBufWriteTextContentBuffer  = &fileContent
    gIntTextfileCodepage = codepage
    gBoolAppendTextFile = bAppend
    
    noError()    
    string msgEval = eval_ gStrWriteBufferCode
    string strErr = lastError()
    if (msgEval != "") return msgEval 
    return strErr 
}


string gStrFileReadCode = "
    // we use that double pointer to not have to copy the buffer contents
    Buffer **bufTextContentBufferDblPtr  = addr_ " ((addr_ (&gBufWriteTextContentBuffer)) int) "
    Buffer bufTextFilenameBuffer = (addr_ " ((addr_ gBufTextFilenameBuffer) int) ") Buffer
    int &iCodepage = addr_ " ((addr_ (&gIntTextfileCodepage)) int) "
    Buffer &bufText = **bufTextContentBufferDblPtr
    
    Stream is = read (bufTextFilenameBuffer \"\", iCodepage)
    
    Buffer bufInput = create(1000000)
    // Iterate over all content of the file
    while (true)
    {
        is >> bufInput
        
        // Process data if some could be read of stream is reached
        if (length bufInput > 0) {         
            combine(bufText, bufInput, 0)
        }
        
        // Prepare next iteration
        setempty( bufInput )
        
        if (end of is) break
    }

    delete( bufInput )
"

string readFileWithoutLeak (string file_Name, Buffer fileContent, int codepage) {
    gBufTextFilenameBuffer = file_Name
    gBufWriteTextContentBuffer  = &fileContent
    gIntTextfileCodepage = codepage
    
    noError()    
    string msgEval = eval_ gStrFileReadCode
    string strErr = lastError()
    if (msgEval != "") return msgEval 
    return strErr 
}
