from cffi import FFI

ffi = FFI()
ffi.set_source("_lz4", """
#define LZ4F_DISABLE_OBSOLETE_ENUMS
#include <lz4frame.h>""", libraries=['lz4'])

ffi.cdef("""
typedef enum {
    LZ4F_default=0,
    LZ4F_max64KB=4,
    LZ4F_max256KB=5,
    LZ4F_max1MB=6,
    LZ4F_max4MB=7
} LZ4F_blockSizeID_t;

typedef enum {
    LZ4F_blockLinked=0,
    LZ4F_blockIndependent
} LZ4F_blockMode_t;

typedef enum {
    LZ4F_noContentChecksum=0,
    LZ4F_contentChecksumEnabled
} LZ4F_contentChecksum_t;

typedef enum {
    LZ4F_frame=0,
    LZ4F_skippableFrame
} LZ4F_frameType_t;

typedef struct {
  LZ4F_blockSizeID_t     blockSizeID;           /* max64KB, max256KB, max1MB, max4MB ; 0 == default */
  LZ4F_blockMode_t       blockMode;             /* blockLinked, blockIndependent ; 0 == default */
  LZ4F_contentChecksum_t contentChecksumFlag;   /* noContentChecksum, contentChecksumEnabled ; 0 == default  */
  LZ4F_frameType_t       frameType;             /* LZ4F_frame, skippableFrame ; 0 == default */
  unsigned long long     contentSize;           /* Size of uncompressed (original) content ; 0 == unknown */
  unsigned               reserved[2];           /* must be zero for forward compatibility */
} LZ4F_frameInfo_t;

typedef struct {
LZ4F_frameInfo_t frameInfo;
int compressionLevel;
unsigned autoFlush;
unsigned reserved[4];
} LZ4F_preferences_t;
""")

ffi.cdef("""
typedef size_t LZ4F_errorCode_t;
unsigned LZ4F_isError(LZ4F_errorCode_t code);
const char* LZ4F_getErrorName(LZ4F_errorCode_t code);
""")

ffi.cdef("size_t LZ4F_compressFrameBound(size_t srcSize, const LZ4F_preferences_t* preferencesPtr);")
ffi.cdef("size_t LZ4F_compressFrame(void* dstBuffer, size_t dstMaxSize, const void* srcBuffer, size_t srcSize, const LZ4F_preferences_t* preferencesPtr);")

ffi.cdef("""
typedef struct LZ4F_cctx_s* LZ4F_compressionContext_t;
typedef struct {
  unsigned stableSrc;    /* 1 == src content will remain available on future calls to LZ4F_compress(); avoid saving src content within tmp buffer as future dictionary */
  unsigned reserved[3];
} LZ4F_compressOptions_t;
""")

ffi.cdef("""
#define LZ4F_VERSION 100
LZ4F_errorCode_t LZ4F_createCompressionContext(LZ4F_compressionContext_t* cctxPtr, unsigned version);
LZ4F_errorCode_t LZ4F_freeCompressionContext(LZ4F_compressionContext_t cctx);
""")


ffi.cdef("""
size_t LZ4F_compressBegin(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const LZ4F_preferences_t* prefsPtr);
size_t LZ4F_compressBound(size_t srcSize, const LZ4F_preferences_t* prefsPtr);
size_t LZ4F_compressUpdate(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const void* srcBuffer, size_t srcSize, const LZ4F_compressOptions_t* cOptPtr);
size_t LZ4F_flush(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const LZ4F_compressOptions_t* cOptPtr);
size_t LZ4F_compressEnd(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const LZ4F_compressOptions_t* cOptPtr);""")

ffi.cdef("""
typedef struct LZ4F_dctx_s* LZ4F_decompressionContext_t;

typedef struct {
  unsigned stableDst;       /* guarantee that decompressed data will still be there on next function calls (avoid storage into tmp buffers) */
  unsigned reserved[3];
} LZ4F_decompressOptions_t;""")

# Resource management
ffi.cdef("""
LZ4F_errorCode_t LZ4F_createDecompressionContext(LZ4F_decompressionContext_t* dctxPtr, unsigned version);
LZ4F_errorCode_t LZ4F_freeDecompressionContext(LZ4F_decompressionContext_t dctx);
""")

ffi.cdef("""
size_t LZ4F_getFrameInfo(LZ4F_decompressionContext_t dctx,
                         LZ4F_frameInfo_t* frameInfoPtr,
                         const void* srcBuffer, size_t* srcSizePtr);

size_t LZ4F_decompress(LZ4F_decompressionContext_t dctx,
                       void* dstBuffer, size_t* dstSizePtr,
                       const void* srcBuffer, size_t* srcSizePtr,
                       const LZ4F_decompressOptions_t* dOptPtr);
""")


if __name__ == "__main__":
    ffi.compile()
