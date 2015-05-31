package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.ContentResolver;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;

import cn.edu.tsinghua.thss.popcorn.R;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class ReportFragment extends Fragment {
    Button open_camera_btn, browse_btn;
    ImageView  image_view;

    private static final int TAKE_PICTURE = 1;
    private static final int BROWSE = 2;

    // 获取sd卡根目录地址,并创建图片父目录文件对象和文件的对象;
    String file_str = Environment.getExternalStorageDirectory().getPath();
    String file_path = file_str + "/willwings/photos";
    File mars_file = new File(file_path);
    File file_go = null;

	@Override
	public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
		super.onCreateView(inflater, container, savedInstanceState);
		View repairView = inflater.inflate(R.layout.activity_tab_report, container,false);
        open_camera_btn = (Button) repairView.findViewById(R.id.id_tab_repair_camera);
        browse_btn = (Button) repairView.findViewById(R.id.id_tab_repair_browse);

        image_view = (ImageView) repairView.findViewById(R.id.id_tab_repair_img);

        //拍照
        open_camera_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // 验证sd卡是否正确安装：
                if (Environment.MEDIA_MOUNTED.equals(Environment
                        .getExternalStorageState())) {
                    // 先创建父目录，如果新创建一个文件的时候，父目录没有存在，那么必须先创建父目录，再新建文件。
                    boolean isSuccessful = true;
                    if (!mars_file.exists()) {
                        isSuccessful  = mars_file.mkdirs();
                    }
                    // 设置跳转的系统拍照的activity为：MediaStore.ACTION_IMAGE_CAPTURE ;
                    Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    file_go = new File(file_path+"/"+System.currentTimeMillis()+".jpg");
                    intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file_go));
                    //跳转到拍照界面;
                    startActivityForResult(intent, TAKE_PICTURE);
                } else {
                    Toast.makeText(getActivity(), "请先安装好SD卡",Toast.LENGTH_LONG).show();
                }
            }
        });

        // 读取本地图片
        browse_btn.setOnClickListener(new Button.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent();
                /* 开启Pictures画面Type设定为image */
                intent.setType("image/*");
                /* 使用Intent.ACTION_GET_CONTENT这个Action */
                intent.setAction(Intent.ACTION_GET_CONTENT);
                /* 取得相片后返回本画面 */
                startActivityForResult(intent, BROWSE);
            }

        });

        return repairView;
	}


    //拍照结束后显示图片;
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        // 判断请求码和结果码是否正确，如果正确的话就显示刚刚所拍照的图片;
        if (resultCode == getActivity().RESULT_OK){
            if(requestCode == TAKE_PICTURE){
                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize = 2;
                Bitmap bmpDefaultPic = BitmapFactory.decodeFile(file_go.getPath(), options);
                image_view.setImageBitmap(bmpDefaultPic);
            }else if(requestCode == BROWSE) {
                Uri uri = data.getData();
                ContentResolver cr = getActivity().getContentResolver();
                try {
                    Bitmap bitmap = BitmapFactory.decodeStream(cr.openInputStream(uri));
                    image_view.setImageBitmap(bitmap);
                } catch (FileNotFoundException e) {
                    Log.e("Exception", e.getMessage(),e);
                }
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }
	
	@Override
	public void onActivityCreated(Bundle savedInstanceState){
		super.onActivityCreated(savedInstanceState);
	}
}
